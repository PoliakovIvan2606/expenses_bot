import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import parse_mode
from aiogram.methods import delete_message
from aiogram.types import Message, message
from aiogram.filters import Command
import logging 

from keyboards import start_keyboard, add_kyeboard_category, delete_product
import database
import exceptions

logging.basicConfig(level=logging.INFO)

TOKEN = "7501798547:AAGvtk56v6bXAV4pm9HhEoG1UB5ap3324FY"

# Создаем бота, диспетчер и роутер
bot = Bot(token=TOKEN)
dp = Dispatcher()

CATEGORIES = database.get_dict_categories()
CODENAME_CAT = [cat[0] for cat in CATEGORIES]
NAME_CAT = [cat[1] for cat in CATEGORIES]


def parse_message(message: str) -> tuple[str, int]:
    data = message.split(' ')
    try:
        data[-1] = int(data[-1])
        return (' '.join(data[0:-1]), data[-1])
    except:
        raise exceptions.NotCorrectMessage()

# ------------------------ Старт --------------------------------
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет, я твой бот для хранения расходов, выбери действие", reply_markup=start_keyboard())

# -------------------- Добавление данных -------------------------
is_add = ''
is_add_category = False

@dp.message(lambda message: message.text == "Добавить")
async def add_btn(message: Message):
    await delete_messages(message, 2)
    await message.answer("Категории", reply_markup=add_kyeboard_category())


@dp.callback_query(lambda c: c.data in CODENAME_CAT)
async def add_eat(query: types.CallbackQuery):
    global is_add
    is_add = query.data
    await query.message.edit_text("Добавь данные")

@dp.message(lambda message: is_add)
async def add_message_data(message: Message):
    try:
        name, price = parse_message(message.text)
        global is_add
        database.add_data_db(name, price, is_add)
        await message.answer(text="Выбери опцию:", reply_markup=start_keyboard())
        is_add = ''
    except exceptions.NotCorrectMessage:
        await message.answer("Введитие правильные данные", reply_markup=add_kyeboard_category())
    finally:
        await delete_messages(message, 2)

async def delete_messages(message: Message, count: int = 3):
    chat_id = message.chat.id

    for msg_id in range(message.message_id, message.message_id - count, -1):
        try:
            await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception as e:
            print(f"Не удалось удалить сообщение {msg_id}: {e}")

@dp.callback_query(lambda c: c.data == 'Add_category')
async def add_category(query: types.CallbackQuery):
    global is_add_category
    is_add_category = True
    await query.message.edit_text("Добавь категорию")

@dp.message(lambda message: is_add_category)
async def add_name_category(message: Message):
    nams_cat = message.text.split(' ')
    database.add_category(nams_cat[1], nams_cat[0])
    await message.answer("Категория была добавлена", reply_markup=start_keyboard())

# ---------------------- Просмотр данных ---------------------------
@dp.message(lambda message: message.text == "Смотреть")
async def link_db(message: Message):
    await delete_messages(message, 2)
    sum_product = 0
    result = ''
    db_dict = database.get_dict_products()
    print(db_dict)
    for category, items in db_dict.items():
        sum_category = 0
        result += f"<b>{category}</b>:\n"
        for item in items:
            result += f" - {item[0]}) {item[1]}: {item[2]} руб.\n"
            sum_category += item[2]
        result += f"<i>Сумма: {sum_category}</i>\n\n"
        sum_product += sum_category
    result += f"\n<b>Всего</b>: {sum_product}"
    await message.answer(result, reply_markup=start_keyboard(), parse_mode='HTML') if result else await message.answer("Данных нет", replay_markup=start_keyboard())

is_delete_product = False
@dp.message(Command("del"))
async def func_delete_product(message: Message):
    global is_delete_product
    is_delete_product = True
    await message.answer("Выберете какой продукт будет удалён")

@dp.message(lambda message: is_delete_product)
async def add_name_category(message: Message):
    database.del_product(message.text)
    sum_product = 0
    result = ''
    db_dict = database.get_dict_products()
    print(db_dict)
    for category, items in db_dict.items():
        sum_category = 0
        result += f"<b>{category}</b>:\n"
        for item in items:
            result += f" - {item[0]}) {item[1]}: {item[2]} руб.\n"
            sum_category += item[2]
        result += f"<i>Сумма: {sum_category}</i>\n\n"
        sum_product += sum_category
    result += f"\n<b>Всего</b>: {sum_product}"

    await delete_messages(message, count=4)
    await message.answer(result, parse_mode='HTML', reply_markup=start_keyboard())

async def main():
    await dp.start_polling(bot)    

if __name__ == '__main__':
    asyncio.run(main())
