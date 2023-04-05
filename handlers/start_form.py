from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from Sost_mach import test_ant
import sqlite3


connect = sqlite3.connect('users.db', check_same_thread=False)
cursor = connect.cursor()


# @dp.message_handler(commands=["start"])
async def start(message: types.Message,state:FSMContext):
    select_id = f"SELECT id FROM logins_ids WHERE id = {message.from_user.id}"
    cursor.execute(select_id)
    ids = cursor.fetchone()
    if len(ids) == 0:
        await message.reply("Здравствуйте. Ваш ID добавлен в нашу базу данных")
        await state.update_data(answer0=message.from_user.id)
        await wait_age(message,state)
    else:
        await message.reply("Ваш id уже есть в базе данных. Вы зарегистрированы.")


async def wait_age(message,state: FSMContext):
    await message.answer("Пожалуйста, напишите Ваш возраст.")
    await state.set_state(test_ant.qu_age)


# @dp.message_handler(state=test_ant.qu_age)
async def db_insert_age(message: types.Message,state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    await wait_weight(message)


async def wait_weight(message):
    await message.answer("Пожалуйста, напишите Ваш вес.")
    await test_ant.qu_weight.set()


# @dp.message_handler(state=test_ant.qu_weight)
async def db_insert_weight(message: types.Message,state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)
    await wait_heaight(message)


async def wait_heaight(message):
    await message.answer("Пожалуйста, напишите Ваш рост.")
    await test_ant.qu_height.set()


# @dp.message_handler(state=test_ant.qu_height)
async def db_insert_height(message: types.Message,state: FSMContext):
    answer = message.text
    await state.update_data(answer3=answer)
    await wait_sex(message)


async def wait_sex(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sex_button1 = types.KeyboardButton(text='Men')
    sex_button2 = types.KeyboardButton(text='Women')
    markup1.add(sex_button1, sex_button2)
    await message.answer(text="Пожалуйста, выберите Ваш пол.",reply_markup=markup1)
    await test_ant.qu_sex.set()


# @dp.message_handler(state=test_ant.qu_sex)
async def db_insert_sex(message: types.Message,state: FSMContext):
    answer = message.text
    await state.update_data(answer4=answer)
    await wait_activity(message)


async def wait_activity(message):
    markup_act = types.ReplyKeyboardMarkup(resize_keyboard=True)
    activity_button1 = types.KeyboardButton(text='Low')
    activity_button2 = types.KeyboardButton(text='Middle')
    activity_button3 = types.KeyboardButton(text='Hight')
    markup_act.add(activity_button1, activity_button2, activity_button3)
    await message.answer(text="Пожалуйста, выберите уровень вашей активности.", reply_markup=markup_act)
    await test_ant.qu_activity.set()


# @dp.message_handler(state=test_ant.qu_activity)
async def db_insert_activity(message: types.Message,state: FSMContext):
    answer = message.text
    await state.update_data(answer5=answer)
    await norm_calories(message, state)


async def norm_calories(message,state: FSMContext):
    data = await state.get_data()
    id = data.get("answer0")
    age = data.get("answer1")
    weight = data.get("answer2")
    height = data.get("answer3")
    sex = data.get("answer4")
    activity = data.get("answer5")
    records = [id,age,weight,height,sex,activity]
    if records[4] == "Men":
        norm_men = 88.36 + (13.4 * int(records[2])) + (4.8 * int(records[3])) - (5.7 * int(records[1]))
        await message.answer(f"ваша базальная норма калорий = {norm_men}")
        if records[5] == "low":
            await message.answer(f"с учетом вашей активности = {norm_men * 1.2}")
            cursor.execute(
            "INSERT INTO logins_ids VALUES (?,?,?,?,?,?,?)",[id,age,weight,height,sex,activity,norm_men * 1.2])
        elif records[5] == "middle":
            await message.answer(f"с учетом вашей активности = {norm_men * 1.55}")
            cursor.execute(
                "INSERT INTO logins_ids VALUES (?,?,?,?,?,?,?)",[id,age,weight,height,sex,activity,norm_men * 1.55])
        else:
            await message.answer(f"с учетом вашей активности = {norm_men * 1.725}")
            cursor.execute(
                "INSERT INTO logins_ids VALUES (?,?,?,?,?,?,?)",[id,age,weight,height,sex,activity,norm_men * 1.725])
    else:
        norm_women = 447.6 + (9.2 * int(records[2])) + (3.1 * int(records[3])) - (4.3 * int(records[1]))
        await message.answer(f"ваша базальная норма калорий = {norm_women}")
        if records[5] == "low":
            await message.answer(f"с учетом вашей активности = {norm_women * 1.2}")
            cursor.execute(
                "INSERT INTO logins_ids VALUES (?,?,?,?,?,?,?)",[id,age,weight,height,sex,activity,norm_women * 1.2])
        elif records[5] == "middle":
            await message.answer(f"с учетом вашей активности = {norm_women * 1.55}")
            cursor.execute(
                "INSERT INTO logins_ids VALUES (?,?,?,?,?,?,?)",[id,age,weight,height,sex,activity,norm_women * 1.55])
        else:
            await message.answer(f"с учетом вашей активности = {norm_women * 1.725}")
            cursor.execute(
                "INSERT INTO logins_ids VALUES (?,?,?,?,?,?,?)",[id,age,weight,height,sex,activity,norm_women * 1.725])
    connect.commit()
    await state.finish()
    from handlers.menu import menu
    await menu(message)


def register_handlers_start_form(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(db_insert_age, state=test_ant.qu_age)
    dp.register_message_handler(db_insert_weight, state=test_ant.qu_weight)
    dp.register_message_handler(db_insert_height, state=test_ant.qu_height)
    dp.register_message_handler(db_insert_sex, state=test_ant.qu_sex)
    dp.register_message_handler(db_insert_activity, state=test_ant.qu_activity)
