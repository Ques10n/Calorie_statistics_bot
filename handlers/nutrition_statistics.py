from aiogram import Dispatcher, types, filters
from aiogram.dispatcher import FSMContext
from Sost_mach import test_ant
import sqlite3
from handlers.create_bot import dp,bot
from datetime import datetime


connect = sqlite3.connect('users.db', check_same_thread=False)
cursor = connect.cursor()


async def stat_wait():
    await test_ant.qu_add.set()


async def add_product_results(state: FSMContext, page_number: int):
    data = await state.get_data()
    request = data.get("answer6")
    sqlite3_select = f"SELECT * FROM produkts WHERE name LIKE '%{request}%'"
    cursor.execute(sqlite3_select)
    records = cursor.fetchall()

    list1 = []
    max_per_page = 10
    step = 1
    if len(records) != 0:
        if len(records) - (max_per_page * page_number + 1) > 10:
            list1.append(f"Результаты {(page_number * max_per_page) + 1} - {max_per_page * (page_number + 1)} из {len(records)}\n"
                     f"\n")
            for i in range(page_number * max_per_page, page_number * max_per_page + max_per_page):
                (name, cal, prot, fats, car) = records[i]
                list1.append(f"*{step})* {name} | *{cal[:4]}* {cal[-4:]} | *{prot[:-1]}*  {prot[-1:]} | *{fats[:-1]}* {fats[-1:]} | *{car[:-1]}* {car[-1:]}\n")
                step += 1
        else:
            list1.append(f"Результаты {(page_number * max_per_page) + 1} - {len(records)} из {len(records)}\n"
                     f"\n")
            for i in range(1, len(records) - max_per_page * page_number):
                (name, cal, prot, fats, car) = records[i]
                list1.append(f"*{step})* {name} | *{cal[:4]}* {cal[-4:]} | *{prot[:-1]}*  {prot[-1:]} | *{fats[:-1]}* {fats[-1:]} | *{car[:-1]}* {car[-1:]}\n")
                step += 1
    else:
        list1 += "Что то пошло не так. Мы ничего не нашли, пожалуйста введите запрос точнее или проверьте регистр."

    return list1


async def get_add_keyboard(quantity: int):
    buttons = [
        types.InlineKeyboardButton(text="⬅", callback_data="add_left"),
        types.InlineKeyboardButton(text="❌", callback_data="add_del"),
        types.InlineKeyboardButton(text="➡", callback_data="add_right"),
    ]
    number_buttons = []
    for i in range(1, quantity):
        number_buttons.append(types.InlineKeyboardButton(text=f"{i}", callback_data=f"add_{i}"))
    keyboard = types.InlineKeyboardMarkup(row_width=5).add(*buttons)
    keyboard.add(*number_buttons)
    return keyboard


async def update_add_text(message: types.Message, new_value: int, state: FSMContext):
    data = await state.get_data()
    request = data.get("answer6")
    len_list = await add_product_results(state, new_value)
    await message.edit_text(text= "".join(len_list) + "\n" \
                 "Что бы выйти из состояния поиска нажмите на ❌",parse_mode="Markdown",
                            reply_markup=await get_add_keyboard(len(len_list)))


@dp.message_handler(state=test_ant.qu_add)
async def get_add_message(message: types.Message,state: FSMContext):
    answer = message.text
    await state.update_data(answer6=answer)
    len_list = await add_product_results(state, 0)
    user_add_data[message.from_user.id] = 0
    await message.answer(text= "".join(len_list) + "\n" \
                 "Что бы выйти из состояния поиска нажмите на ❌",parse_mode="Markdown",reply_markup=await get_add_keyboard(len(len_list)))


async def wait_grams(message: types.Message):
    await message.answer("Пожалуйста напишите сколько вы сьели в граммах")
    await test_ant.qu_grams.set()


@dp.message_handler(state=test_ant.qu_grams)
async def db_insert_grams(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer_gram=answer)
    data = await state.get_data()
    product = data.get("prod_in_db")
    grams = data.get("answer_gram")
    cursor.execute(
        "INSERT INTO accounting_kcal VALUES (?,?,?,?)",
        [message.from_user.id, product, datetime.now(), grams])
    connect.commit()
    await state.finish()
    await message.answer("Спасибо")
    await stat_wait()


async def add_inser_db(call: types.CallbackQuery, state: FSMContext,add_number, user_value):
    data = await state.get_data()
    grams = data.get("answer_gram")
    print(grams)
    add = await add_product_results(state=state, page_number=user_value)
    add_work = add[add_number].split("|")
    await state.update_data(prod_in_db=add_work[0][4:-1])
    await wait_grams(message=call.message)


user_add_data = {}


@dp.callback_query_handler(filters.Text(startswith="add_"),state=test_ant.qu_add)
async def search_s(call: types.CallbackQuery,state: FSMContext):
    user_value = user_add_data.get(call.from_user.id, 0)
    action = call.data.split("_")[1]
    if action == "left":
        user_add_data[call.from_user.id] = user_value - 1
        await update_add_text(call.message, new_value=user_value - 1,state=state)
    elif action == "right":
        user_add_data[call.from_user.id] = user_value + 1
        await update_add_text(call.message, new_value= user_value + 1,state=state)
    elif action == "del":
        await call.message.delete()
        await state.finish()

        from handlers.menu import menu
        await menu(call.message)
    else:
        await add_inser_db(call=call, state=state, add_number=int(action), user_value=user_value)


def register_stat_handlers(dp: Dispatcher):
    dp.register_message_handler(get_add_message, state=test_ant.qu_add)
    dp.register_message_handler(db_insert_grams, state=test_ant.qu_grams)
    dp.register_callback_query_handler(search_s,filters.Text(startswith="add_"),state=test_ant.qu_add)