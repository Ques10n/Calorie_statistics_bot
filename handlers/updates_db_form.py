import sqlite3
from aiogram import filters, types, Dispatcher
from handlers.create_bot import dp,bot
from aiogram.dispatcher import FSMContext
from Sost_mach import test_ant
# from handlers.menu import register_menu_handlers


connect = sqlite3.connect('users.db', check_same_thread=False)
cursor = connect.cursor()


@dp.message_handler(commands=["update"])
async def update_datas(message):
    markup_act = types.ReplyKeyboardMarkup(resize_keyboard=True)
    update_button1 = types.KeyboardButton(text="Изменить возраст")
    update_button2 = types.KeyboardButton(text="Изменить рост")
    update_button3 = types.KeyboardButton(text="Изменить вес")
    update_button4 = types.KeyboardButton(text="Изменить уровень активности")
    update_button5 = types.KeyboardButton(text="Вернуться в меню")
    markup_act.add(update_button1,update_button2,update_button3,update_button4,update_button5)
    await message.answer(text="Выберите что хотите изменить",reply_markup=markup_act)



# @dp.message_handler(filters.Text(contains="Изменить возраст"))
async def wait_new_age(message: types.Message, state: FSMContext):
    await message.answer("Введите новое значение")
    await state.set_state(test_ant.qu_up_age)


# @dp.message_handler(state=test_ant.qu_age)
async def update_age(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer_up=answer)
    data = await state.get_data()
    new_val = data.get("answer_up")
    cursor.execute(f"UPDATE logins_ids SET age = {new_val}")
    connect.commit()
    await state.finish()
    await norm_calories(message, state)
    await update_datas(message)


# @dp.message_handler(filters.Text(contains="Изменить рост"))
async def wait_new_height(message: types.Message, state: FSMContext):
    await message.answer("Введите новое значение")
    await state.set_state(test_ant.qu_up_height)


# @dp.message_handler(state=test_ant.qu_height)
async def update_height(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer_up=answer)
    data = await state.get_data()
    new_val = data.get("answer_up")
    cursor.execute(f"UPDATE logins_ids SET height = {new_val}")
    connect.commit()
    await state.finish()
    await norm_calories(message, state)
    await update_datas(message)


# @dp.message_handler(filters.Text(contains="Изменить вес"))
async def wait_new_weight(message: types.Message, state: FSMContext):
    await message.answer("Введите новое значение")
    await state.set_state(test_ant.qu_up_weight)


# @dp.message_handler(state=test_ant.qu_weight)
async def update_weight(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer_up=answer)
    data = await state.get_data()
    new_val = data.get("answer_up")
    cursor.execute(f"UPDATE logins_ids SET weight = {new_val}")
    connect.commit()
    await state.finish()
    await norm_calories(message, state)
    await update_datas(message)


# @dp.message_handler(filters.Text(contains="Изменить уровень активности"))
async def wait_new_activity(message: types.Message, state: FSMContext):
    markup_act = types.ReplyKeyboardMarkup(resize_keyboard=True)
    activity_button1 = types.KeyboardButton(text='Low')
    activity_button2 = types.KeyboardButton(text='Middle')
    activity_button3 = types.KeyboardButton(text='Hight')
    markup_act.add(activity_button1, activity_button2, activity_button3)
    await message.answer("Введите новое значение", reply_markup=markup_act)
    await state.set_state(test_ant.qu_up_activity)


# @dp.message_handler(state=test_ant.qu_activity)
async def update_activity(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer_up=answer)
    data = await state.get_data()
    new_val = data.get("answer_up")
    cursor.execute(f"UPDATE logins_ids SET activity = '{new_val}'")
    connect.commit()
    await state.finish()
    await norm_calories(message, state)
    await update_datas(message)


async def norm_calories(message,state: FSMContext):
    sqlite3_select = f"SELECT * FROM logins_ids WHERE id = {message.from_user.id}"
    cursor.execute(sqlite3_select)
    records = cursor.fetchall()
    if records[0][4] == "Men":
        norm_men = 88.36 + (13.4 * int(records[0][2])) + (4.8 * int(records[0][3])) - (5.7 * int(records[0][1]))
        await message.answer(f"ваша базальная норма калорий = {norm_men}")
        if records[0][5] == "Low":
            await message.answer(f"с учетом вашей активности = {norm_men * 1.2}")
            cursor.execute(
            f"UPDATE logins_ids SET cal_today = {norm_men * 1.2} WHERE id = {message.from_user.id}")
        elif records[0][5] == "Middle":
            await message.answer(f"с учетом вашей активности = {norm_men * 1.55}")
            cursor.execute(
                f"UPDATE logins_ids SET cal_today = {norm_men * 1.55} WHERE id = {message.from_user.id}")
        else:
            await message.answer(f"с учетом вашей активности = {norm_men * 1.725}")
            cursor.execute(
                f"UPDATE logins_ids SET cal_today = {norm_men * 1.725} WHERE id = {message.from_user.id}")
    else:
        norm_women = 447.6 + (9.2 * int(records[0][2])) + (3.1 * int(records[0][3])) - (4.3 * int(records[0][1]))
        await message.answer(f"ваша базальная норма калорий = {norm_women}")
        if records[0][5] == "Low":
            await message.answer(f"с учетом вашей активности = {norm_women * 1.2}")
            cursor.execute(
                f"UPDATE logins_ids SET cal_today = {norm_women * 1.2} WHERE id = {message.from_user.id}")
        elif records[0][5] == "Middle":
            await message.answer(f"с учетом вашей активности = {norm_women * 1.55}")
            cursor.execute(
                f"UPDATE logins_ids SET cal_today = {norm_women * 1.55} WHERE id = {message.from_user.id}")
        else:
            await message.answer(f"с учетом вашей активности = {norm_women * 1.725}")
            cursor.execute(
                f"UPDATE logins_ids SET cal_today = {norm_women * 1.725} WHERE id = {message.from_user.id}")
    connect.commit()
    await state.finish()


async def backto_menu(message: types.Message):
    from handlers.menu import menu
    await menu(message)


def register_handlers_update_db(dp: Dispatcher):
    dp.register_message_handler(update_datas, commands=["update"])
    dp.register_message_handler(wait_new_age, filters.Text(contains="Изменить возраст"))
    dp.register_message_handler(update_age, state=test_ant.qu_up_age)
    dp.register_message_handler(wait_new_height, filters.Text(contains="Изменить рост"))
    dp.register_message_handler(update_height, state=test_ant.qu_up_height)
    dp.register_message_handler(wait_new_weight, filters.Text(contains="Изменить вес"))
    dp.register_message_handler(update_weight, state=test_ant.qu_up_weight)
    dp.register_message_handler(wait_new_activity, filters.Text(contains="Изменить уровень активности"))
    dp.register_message_handler(update_activity, state=test_ant.qu_up_activity)
    dp.register_message_handler(backto_menu, filters.Text(contains="Вернуться в меню"))