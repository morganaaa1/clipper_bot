import os
from bot_instance import client

def convert_to_seconds(time_str):
    try:
        time_str = str(time_str).strip()
        if ":" in time_str:
            parts = time_str.split(':')
            if len(parts) == 2: return int(parts[0]) * 60 + int(parts[1])
            if len(parts) == 3: return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return int(float(time_str))
    except:
        return 0

async def analyze_video_with_groq(audio_path):
    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(audio_path, file.read()),
            model="whisper-large-v3",
            response_format="verbose_json",
        )
    
    full_text = transcription.text
    print(f"--- DEBUG: Transkrip Berhasil Diambil ---")

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system", 
                "content": (
                    "Kamu adalah editor video. Analisis transkrip ini. "
                    "Berikan 3 momen paling penting dengan durasi 60-120 detik per klip. "
                    "Format WAJIB: [START-END] | [JUDUL]. "
                    "Contoh: 150-240 | Bahasan Kurma. "
                    "Pastikan START dan END adalah angka detik yang sesuai dengan isi bahasannya."
                )
            },
            {"role": "user", "content": f"Transkrip: {full_text}"}
        ],
        model="llama-3.3-70b-versatile",
    )
    
    ai_response = chat_completion.choices[0].message.content
    print(f"--- DEBUG AI RESPONSE ---\n{ai_response}\n------------------------")
    return ai_response