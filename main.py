from aiogram.utils import executor
from handlers.create_bot import dp
from handlers import start_form, menu, updates_db_form, nutrition_statistics, mailing
from aiogram import Dispatcher


async def on_startup(dp: Dispatcher):
    print("bot is started")
    mailing.schedule_start(dp=dp)



start_form.register_handlers_start_form(dp)
menu.register_menu_handlers(dp)
updates_db_form.register_handlers_update_db(dp)
# nutrition_statistics.register_stat_handlers(dp)
# search_product.register_search_product_handlers(dp)


executor.start_polling(dp, skip_updates=False,on_startup=on_startup)