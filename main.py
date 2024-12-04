import asyncio
from os import stat
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import logging 

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from keyboards import start_keyboard, add_kyeboard_category, add_transport
import database
import exceptions
import utils

# from routers.add_expenses import router as expenses_router

logging.basicConfig(level=logging.INFO)

TOKEN = "7501798547:AAGvtk56v6bXAV4pm9HhEoG1UB5ap3324FY"

# Создаем бота, диспетчер и роутер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# dp.include_router(expenses_router)

# Global
CODENAME_CAT = [cat[0] for cat in database.get_dict_categories()]


# ------------------------ Старт --------------------------------
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет, я твой бот для хранения расходов, выбери действие", reply_markup=start_keyboard())

# ---------------- Добавление данных расхода ----------------

class Form(StatesGroup):
    category = State()
    product = State()

    is_add_category = State()
    
    delete_data = State()
    
    income = State()

@dp.message(lambda message: message.text == "Расходы")
async def add_btn(message: Message):
    await utils.delete_messages(message, 2)
    await message.answer("Категории", reply_markup=add_kyeboard_category())

@dp.callback_query(lambda c: c.data == 'Add_category')
async def add_category(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text('Добавь категорию, например "Озон ozon"')
    await state.set_state(Form.is_add_category)

@dp.message(StateFilter(Form.is_add_category))
async def add_name_category(message: Message, state: FSMContext):
    nams_cat = message.text.split(' ')
    database.add_category(nams_cat[1], nams_cat[0])
    global CODENAME_CAT
    CODENAME_CAT = [cat[0] for cat in database.get_dict_categories()]
    await message.answer("Категория была добавлена", reply_markup=start_keyboard())
    await utils.delete_messages(message, 2)
    await state.clear()

@dp.callback_query(lambda c: c.data in CODENAME_CAT)
async def add_eat(query: types.CallbackQuery, state: FSMContext):    
    await state.set_data({'category': query.data})
    reply_markup = add_transport() if query.data == "transport" else None
    await query.message.edit_text("Добавить данные", reply_markup=reply_markup)
    await state.set_state(Form.product)


@dp.callback_query(lambda c: c.data == "prod_bus")
async def add_bus(query: types.CallbackQuery, state: FSMContext):
    database.add_data_db("Автобус", 31, "transport")
    await utils.delete_messages(query.message, 1)
    await state.clear()
    await query.message.answer("Выбери опцию:", reply_markup=start_keyboard())


@dp.message(StateFilter(Form.product))
async def add_message_data(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        name, price = utils.parse_message(message.text)
        database.add_data_db(name, price, data["category"])
        await message.answer(text="Выбери опцию:", reply_markup=start_keyboard())
        await state.clear()
    except exceptions.NotCorrectMessage:
        await message.answer("Введитие правильные данные", reply_markup=add_kyeboard_category())
    finally:
        await utils.delete_messages(message, 2)


# ---------------- Добавление данных дохода -------------------------
@dp.message(lambda message: message.text == "Доходы")
async def add_income_func(message: Message, state: FSMContext):
    await utils.delete_messages(message, 2)
    await message.answer("Введите данные")
    await state.set_state(Form.income)

@dp.message(StateFilter(Form.income))
async def add_message_data(message: Message, state: FSMContext):
    try:
        name, price = utils.parse_message(message.text)
        database.add_income(name, price)
        await message.answer(text="Выбери опцию:", reply_markup=start_keyboard())
        await state.clear()
    except exceptions.NotCorrectMessage:
        await message.answer("Введитие правильные данные", reply_markup=add_kyeboard_category())
    finally:
        await utils.delete_messages(message, 2)


# ---------------------- Просмотр данных ---------------------------
@dp.message(lambda message: message.text == "Смотреть")
async def link_db(message: Message):
    await utils.delete_messages(message, 2)
    result = await utils.get_str_data()
    await message.answer(result, reply_markup=start_keyboard(), parse_mode='HTML') if result else await message.answer("Данных нет", replay_markup=start_keyboard())

@dp.message(Command("del"))
async def func_delete_product(message: Message, state: FSMContext):
    await message.answer("Выберете какой продукт будет удалён")
    await state.set_state(Form.delete_data)

@dp.message(StateFilter(Form.delete_data))
async def add_name_category(message: Message, state: FSMContext):
    database.del_product(message.text)
    result = await utils.get_str_data()
    await utils.delete_messages(message, count=4)
    await message.answer(result, parse_mode='HTML', reply_markup=start_keyboard())
    await state.clear()

async def main():
    await dp.start_polling(bot)    

if __name__ == '__main__':
    asyncio.run(main())
