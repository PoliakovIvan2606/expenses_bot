from aiogram import types
from database import get_dict_categories

def start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Добавить"), types.KeyboardButton(text="Смотреть")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def add_kyeboard_category():
    data_category = get_dict_categories()
    iter_ = 0
    found = False
    lins_dict_keyboards = []
    for line in range(0, len(data_category) // 3 + 1):
        line_keyboard = []
        for id_category in range(0, 3):
            line_keyboard.append(types.InlineKeyboardButton(text=data_category[id_category + 3 * line][1], callback_data=data_category[id_category + 3 * line][0]))
            iter_ += 1
            if iter_ == len(data_category):
                found = True
                break
        lins_dict_keyboards.append(line_keyboard)
        if found:
            break
    lins_dict_keyboards.append([types.InlineKeyboardButton(text='Добавить', callback_data='Add_category')])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=lins_dict_keyboards)
    return keyboard

def delete_product():
    keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="Удалить", callback_data='delete_product')]
                ]
            )
    return keyboard
