import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from Finance import accounts, add, analytics, limits, settings
from FinanceFamily import family_account, family_add, family_analytics, family_limits, family_settings

load_dotenv()
TOKEN = os.environ["TOKEN_BOT"]


async def main() -> None:
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(TOKEN, parse_mode="HTML")

    dp.include_router(family_limits.router)
    dp.include_router(family_analytics.router)
    dp.include_router(family_add.router)
    dp.include_router(family_account.router)
    dp.include_router(settings.router)
    dp.include_router(limits.router)
    dp.include_router(analytics.router)
    dp.include_router(add.router)
    dp.include_router(accounts.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
