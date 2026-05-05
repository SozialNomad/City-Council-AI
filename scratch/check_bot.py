import asyncio
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN

async def check_bot():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    me = await bot.get_me()
    print(f"Bot Name: {me.first_name}")
    print(f"Bot Username: @{me.username}")
    
    updates = await bot.get_updates()
    if updates:
        for update in updates:
            if update.message:
                print(f"Recent Chat ID: {update.message.chat_id} from {update.message.from_user.username}")
    else:
        print("No recent updates/messages found.")

if __name__ == "__main__":
    asyncio.run(check_bot())
