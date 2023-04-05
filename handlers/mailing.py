from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
import sqlite3
from aiogram import types, Dispatcher


scheduler = AsyncIOScheduler()
connect = sqlite3.connect('users.db', check_same_thread=False)
cursor = connect.cursor()


async def id():
    sqlite3_select_ids = f"SELECT id FROM logins_ids"
    cursor.execute(sqlite3_select_ids)
    ids = cursor.fetchall()
    return ids


async def return_stat(dp: Dispatcher):
    ids = await id()
    for i in range(len(ids)):
        sqlite3_select_kcals = f"SELECT product, grams FROM accounting_kcal WHERE date LIKE '%{datetime.date.today()}%' and user_id = {ids[i][0]}"
        cursor.execute(sqlite3_select_kcals)
        records = cursor.fetchall()
        all_kcal = 0
        all_fats = 0
        all_prot = 0
        all_car = 0
        text = "Сегодня вы сьели:\n"

        for j in range(0, len(records)):
            select_cpfc = f"SELECT calories, protein, fats, carbohydrates FROM produkts WHERE name LIKE '%{records[j][0][1:-1]}%'"
            cursor.execute(select_cpfc)
            cpfc = cursor.fetchall()
            try:
                all_kcal += (int(cpfc[0][0][0:-5]) / 100) *  records[j][1]
                all_fats += (float(cpfc[0][2][0:-2].replace(",",".")) / 100) * records[j][1]
                all_car += (float(cpfc[0][3][0:-2].replace(",",".")) / 100) * records[j][1]
                all_prot += (float(cpfc[0][1][0:-2].replace(",",".")) / 100) * records[j][1]
            except:
                pass
        for step in range(1,len(records) + 1):
            text += f"{records[step - 1][0]} в количестве {records[step - 1][1]} грамм \n" \
                    f""
        text += f"Всего: {all_kcal} калорий\n" \
                f"{all_fats} жиров\n" \
                f"{all_car} углеводов\n" \
                f"{all_prot} белков"
        await dp.bot.send_message(chat_id=ids[i][0], text=text)


def schedule_start(dp: Dispatcher):
    scheduler.add_job(func= return_stat, trigger="interval", hours=24, args=(dp, ))
    scheduler.start()