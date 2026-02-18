import os
import asyncio
import re
from aiogram import types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_instance import dp, bot, url_cache
from services import analyze_video_with_groq, convert_to_seconds

@dp.message(F.text.contains("http"))
async def handle_link(message: types.Message):
    url = message.text
    msg = await message.answer("⏳ Menganalisis konten video...")

    audio_file = f"audio_{message.message_id}.mp3"
    proc = await asyncio.create_subprocess_shell(
        f'yt-dlp -x --audio-format mp3 --audio-quality 128k -o "{audio_file}" "{url}"'
    )
    await proc.wait()

    try:
        analysis = await analyze_video_with_groq(audio_file)
        cache_key = str(msg.message_id)
        url_cache[cache_key] = {"url": url, "clips": []}

        builder = InlineKeyboardBuilder()
        lines = analysis.strip().split('\n')
        
        for line in lines:
            match = re.search(r'(\d+)\s*-\s*(\d+)', line)
            if match and "|" in line:
                s, e = match.group(1), match.group(2)
                title = line.split('|')[-1].strip()
                
                url_cache[cache_key]["clips"].append({
                    "start": int(s),
                    "end": int(e),
                    "title": title
                })
                
                idx = len(url_cache[cache_key]["clips"]) - 1
                builder.row(types.InlineKeyboardButton(
                    text=f"🎬 {title[:30]}", 
                    callback_data=f"cut:{cache_key}:{idx}")
                )

        if url_cache[cache_key]["clips"]:
            await msg.edit_text(f"Pilih momen (Durasi 1-2 Menit):\n\n{analysis}", reply_markup=builder.as_markup())
        else:
            await msg.edit_text("AI tidak memberikan format waktu yang jelas. Coba lagi.")

    except Exception as e:
        await msg.edit_text(f"⚠️ Error: {str(e)}")
    finally:
        if os.path.exists(audio_file): os.remove(audio_file)

@dp.callback_query(F.data.startswith("cut:"))
async def process_cut(callback: types.CallbackQuery):
    _, cache_key, idx = callback.data.split(":")
    data = url_cache.get(cache_key)
    
    if not data:
        await callback.answer("Sesi kedaluwarsa.", show_alert=True)
        return

    clip = data["clips"][int(idx)]
    start = clip["start"]
    end = clip["end"]
    judul = clip["title"]

    if (end - start) < 60:
        end = start + 60

    print(f"--- DEBUG CUTTING: Memproses {judul} di {start}-{end} ---")
    await callback.message.edit_text(f"✂️ Memotong: {judul}...")
    
    output_video = f"clip_{cache_key}_{idx}.mp4"
    
    cmd = (
        f'yt-dlp -f "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" '
        f'--download-sections "*{start}-{end}" '
        f'--force-keyframes-at-cuts '
        f'"{data["url"]}" -o "{output_video}"'
    )

    process = await asyncio.create_subprocess_shell(cmd)
    await process.wait()

    if os.path.exists(output_video):
        await callback.message.answer_video(
            video=types.FSInputFile(output_video),
            caption=f"Klip {start}-{end} | {judul} Done 🔥"
        )
        await callback.message.delete()
        os.remove(output_video)
    else:
        await callback.message.answer("❌ Gagal memotong.")