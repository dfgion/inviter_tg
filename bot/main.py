import asyncio

from aiogram import Router, Dispatcher

from core.config import bot, dp
from core.handers import admin, users
from core.middlewares.users import NewUserMiddleware
from core.middlewares.admins import IsAdminMiddleware


def on_startup(dispatcher):
    print('Бот Запущен')
    
def set_user_middleware_router(router: Router):
    router.chat_join_request.middleware.register(NewUserMiddleware())
    return router

def set_admin_middleware_router(router: Router):
    router.message.outer_middleware.register(IsAdminMiddleware())
    router.callback_query.outer_middleware.register(IsAdminMiddleware())
    return router

def dp_setting(dp: Dispatcher) -> None:
    dp.include_router(set_user_middleware_router(users.router))
    dp.include_router(set_admin_middleware_router(admin.router))

async def async_main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(on_startup)
    dp_setting(dp)
    await dp.start_polling(
        bot
    )

if __name__ == "__main__":
    asyncio.run(async_main())