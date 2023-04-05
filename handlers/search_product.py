from aiogram import Dispatcher, types, filters
from aiogram.dispatcher import FSMContext
from Sost_mach import test_ant
import sqlite3
from handlers.create_bot import dp,bot


connect = sqlite3.connect('users.db', check_same_thread=False)
cursor = connect.cursor()


async def wait():
    await test_ant.qu_search.set()


async def get_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="⬅", callback_data="num_left"),
        types.InlineKeyboardButton(text="➡", callback_data="num_right"),
        types.InlineKeyboardButton(text="❌", callback_data="num_del")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


async def results(page_number,state):
    data = await state.get_data()
    request = data.get("answer6")
    sqlite3_select = f"SELECT * FROM produkts WHERE name LIKE '%{request}%'"
    cursor.execute(sqlite3_select)
    connect.commit()
    records = cursor.fetchall()

    list1 = ""
    max_per_page = 10
    if len(records) != 0:
        if len(records) - (max_per_page * page_number + 1) > 10:
            list1 += f"Результаты {(page_number * max_per_page) + 1} - {max_per_page * (page_number + 1)} из {len(records)}\n" \
                     f"\n"
            for i in range(page_number * max_per_page, page_number * max_per_page + max_per_page):
                (name, cal, prot, fats, car) = records[i]
                list1 += f"*{i + 1})* {name} | *{cal[:4]}* {cal[-4:]} | *{prot[:-1]}*  {prot[-1:]} | *{fats[:-1]}* {fats[-1:]} | *{car[:-1]}* {car[-1:]}\n"
            list1 += "\n" \
                     "Что бы выйти из состояния поиска нажмите на ❌"
        else:
            list1 += f"Результаты {(page_number * max_per_page) + 1} - {len(records)} из {len(records)}\n" \
                     f"\n"
            for i in range(max_per_page * page_number, len(records)):
                (name, cal, prot, fats, car) = records[i]
                list1 += f"*{i + 1})* {name} | *{cal[:4]}* {cal[-4:]} | *{prot[:-1]}*  {prot[-1:]} | *{fats[:-1]}* {fats[-1:]} | *{car[:-1]}* {car[-1:]}\n"
            list1 += "\n" \
                     "Что бы выйти из состояния поиска нажмите на ❌"
    else:
        list1 += "Что то пошло не так. Мы ничего не нашли, пожалуйста введите запрос точнее или проверьте регистр."

    return list1


@dp.message_handler(state=test_ant.qu_search)
async def get_message(message: types.Message,state: FSMContext):
    answer = message.text
    await state.update_data(answer6=answer)

    user_data[message.from_user.id] = 0
    await message.answer(text=await results(page_number=0,state=state),parse_mode="Markdown",reply_markup=await get_keyboard())


async def update_num_text(message: types.Message, new_value: int, state: FSMContext):
    await message.edit_text(text=await results(new_value,state=state),parse_mode="Markdown", reply_markup=await get_keyboard())


user_data = {}


@dp.callback_query_handler(filters.Text(startswith="num_"),state=test_ant.qu_search)
async def search_s(call: types.CallbackQuery,state: FSMContext):
    user_value = user_data.get(call.from_user.id, 0)
    action = call.data.split("_")[1]
    if action == "left":
        user_data[call.from_user.id] = user_value - 1
        await update_num_text(call.message, new_value=user_value - 1,state=state)
    elif action == "right":
        user_data[call.from_user.id] = user_value + 1
        await update_num_text(call.message, new_value= user_value + 1,state=state)
    elif action == "del":
        await call.message.delete()
        await state.finish()

        from handlers.menu import menu
        await menu(call.message)
    await call.answer()


# async def register_search_product_handlers(dp: Dispatcher):
#     await wait()
#     dp.message_handler(get_message, state=test_ant.qu_search)
#     dp.callback_query_handler(search_s, filters.Text(startswith="num_"),state=test_ant.qu_search)