import asyncio
import handlers  # Harus diimport agar handler terdaftar
from bot_instance import dp, bot

async def main():
    print("🚀 Bot Clipper Berjalan...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())