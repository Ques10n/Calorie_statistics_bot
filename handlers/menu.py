from aiogram import types, Dispatcher, filters
from handlers.search_product import wait
from handlers.updates_db_form import register_handlers_update_db
from handlers.create_bot import dp
from handlers.nutrition_statistics import stat_wait


# @dp.message_handler(commands=["menu"])
async def menu(message):
    markup_act = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button1 = types.KeyboardButton(text="Изменить свои данные")
    menu_button2 = types.KeyboardButton(text="Калорийность продукта")
    menu_button3 = types.KeyboardButton(text="Добавить сьеденные продукты")
    markup_act.add(menu_button2,menu_button1,menu_button3)
    await message.answer(text='Вы в меню. Выберите что хотите сделать.',reply_markup=markup_act)


# @dp.message_handler(lambda message: message.text == "Изменить свои данные")
async def update(message: types.Message):
    markup_act = types.ReplyKeyboardMarkup(resize_keyboard=True)
    update_button1 = types.KeyboardButton(text="Изменить возраст")
    update_button2 = types.KeyboardButton(text="Изменить рост")
    update_button3 = types.KeyboardButton(text="Изменить вес")
    update_button4 = types.KeyboardButton(text="Изменить уровень активности")
    update_button5 = types.KeyboardButton(text="Вернуться в меню")
    markup_act.add(update_button1, update_button2, update_button3, update_button4, update_button5)
    await message.answer(text="Выберите что хотите изменить", reply_markup=markup_act)
    register_handlers_update_db(dp)


# @dp.message_handler(lambda message: message.text == "Калорийность продукта")
async def search_w(message: types.Message):
    await message.answer("Пожалуйста введите свой запрос.")
    await wait()


# @dp.message_handler(lambda message: message.text == "Добавить сьеденные продукты")
async def search_add(message: types.Message):
    await message.answer("Пожалуйста введите название продукта который вы сьели.")
    await stat_wait()


def register_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(menu, filters.Command(commands=["menu","меню"]))
    dp.register_message_handler(update, lambda message: message.text == "Изменить свои данные")
    dp.register_message_handler(search_w, lambda message: message.text == "Калорийность продукта")
    dp.register_message_handler(search_add, lambda message: message.text == "Добавить сьеденные продукты")
