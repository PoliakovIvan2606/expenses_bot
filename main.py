import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import logging 

from keyboards import start_keyboard, add_kyeboard_category, add_transport
import database
import exceptions
import utils


logging.basicConfig(level=logging.INFO)

TOKEN = "7501798547:AAGvtk56v6bXAV4pm9HhEoG1UB5ap3324FY"

# Создаем бота, диспетчер и роутер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Global
CODENAME_CAT = [cat[0] for cat in database.get_dict_categories()]


# ------------------------ Старт --------------------------------
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет, я твой бот для хранения расходов, выбери действие", reply_markup=start_keyboard())

# -------------------- Добавление данных -------------------------
is_add = ''
is_add_category = False

@dp.message(lambda message: message.text == "Добавить")
async def add_btn(message: Message):
    await utils.delete_messages(message, 2)
    await message.answer("Категории", reply_markup=add_kyeboard_category())


@dp.callback_query(lambda c: c.data in CODENAME_CAT)
async def add_eat(query: types.CallbackQuery):
    global is_add
    is_add = query.data

    reply_markup = add_transport() if query.data == "transport" else None

    await query.message.edit_text("Добавить данные", reply_markup=reply_markup)


is_add_bus = False
@dp.callback_query(lambda c: c.data == "prod_bus")
async def add_bus(query: types.CallbackQuery):
    database.add_data_db("Автобус", 31, "transport")
    global is_add
    is_add = ''
    await utils.delete_messages(query.message, 1)
    await query.message.answer("Выбери опцию:", reply_markup=start_keyboard())


@dp.message(lambda message: is_add)
async def add_message_data(message: Message):
    try:
        name, price = utils.parse_message(message.text)
        global is_add
        database.add_data_db(name, price, is_add)
        await message.answer(text="Выбери опцию:", reply_markup=start_keyboard())
        is_add = ''
    except exceptions.NotCorrectMessage:
        await message.answer("Введитие правильные данные", reply_markup=add_kyeboard_category())
    finally:
        await utils.delete_messages(message, 2)

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
    await utils.delete_messages(message, 2)
    result = await utils.get_str_data()
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
    result = await utils.get_str_data()
    await utils.delete_messages(message, count=4)
    await message.answer(result, parse_mode='HTML', reply_markup=start_keyboard())

async def main():
    await dp.start_polling(bot)    

if __name__ == '__main__':
    asyncio.run(main())
