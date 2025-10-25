import asyncio
import logging

from init_bot import bot, dp
from handlers.admin import admin_router
from handlers.users import user_router
from payment import payment_router

logging.basicConfig(level=logging.INFO)

dp.include_router(admin_router)
dp.include_router(user_router)
dp.include_router(payment_router)
    
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())