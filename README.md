# 🎬 AI-Powered Video Clipper Bot

Bot Telegram cerdas yang mampu mengotomatisasi proses *clipping* video panjang menjadi potongan momen penting berdurasi 60-120 detik menggunakan teknologi AI terbaru dari Groq (Llama 3.3 & Whisper).



## 🚀 Fitur Utama
- **Automated Transcription:** Menggunakan **Whisper Large V3** untuk mengubah audio video menjadi teks secara instan.
- **Intelligent Analysis:** Menggunakan **Llama 3.3 70B** untuk menentukan momen paling relevan dari transkrip.
- **Selective Clipping:** Mengunduh hanya bagian video yang dibutuhkan menggunakan **yt-dlp**, menghemat bandwidth dan penyimpanan.
- **Custom Duration:** Menghasilkan klip dengan durasi ideal (1-2 menit) untuk konteks pembahasan yang utuh.
- **Asynchronous Processing:** Dibangun dengan **Aiogram 3** untuk performa yang responsif.

## 🛠️ Stack Teknologi
- **Bahasa Pemrograman:** Python 3.10+
- **AI Models:** - Groq Llama 3.3 70B (Text Analysis)
  - Groq Whisper Large V3 (Speech-to-Text)
- **Library:** - `aiogram` (Telegram Bot Framework)
  - `groq` (SDK for AI Inference)
- **Tools:**
  - `yt-dlp` (Video Downloader)
  - `FFmpeg` (Video Processing)

## 📋 Prasyarat
Sebelum menjalankan, pastikan Anda memiliki:
- Python 3.10 ke atas.
- FFmpeg terinstall di sistem.
- API Key dari [Groq Console](https://console.groq.com/).
- Bot Token dari [@BotFather](https://t.me/botfather).

## 🔧 Instalasi & Penggunaan

1. **Clone repositori ini:**
   ```bash
   git clone [https://github.com/morganaaa1/clipper_bot.git](https://github.com/morganaaa1/clipper_bot.git)
   cd clipper_bot
