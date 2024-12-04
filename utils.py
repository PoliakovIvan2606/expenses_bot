from aiogram.types import Message
import database
import exceptions
from main import bot

def parse_message(message: str) -> tuple[str, int]:
    data = message.split(' ')
    try:
        data[-1] = int(data[-1])
        return (' '.join(data[0:-1]), data[-1])
    except:
        raise exceptions.NotCorrectMessage()

async def delete_messages(message: Message, count: int = 3):
    chat_id = message.chat.id

    for msg_id in range(message.message_id, message.message_id - count, -1):
        try:
            await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception as e:
            print(f"Не удалось удалить сообщение {msg_id}: {e}")

async def get_str_data():
    sum_product = 0
    result = ''
    result += "<b>РАСХОДЫ</b>\n\n"
    db_dict = database.get_dict_products()
    for category, items in db_dict.items():
        sum_category = 0
        result += f"<b>{category}</b>:\n"
        for item in items:
            result += f" - {item[0]}) {item[1]}: {item[2]} руб.\n"
            sum_category += item[2]
        result += f"<i>Сумма: {sum_category}</i>\n\n"
        sum_product += sum_category
    result += f"<b>Всего</b>: {sum_product}\n\n"

    sum_income = 0
    db_income = database.get_income()
    result += "<b>ДОХОДЫ</b>\n"
    for data in db_income:
        result += f"- {data[0]}: {data[1]}\n"
        sum_income += data[1]
    result += f"<b>Всего</b>: {sum_income}\n\n"

    result += f"<b>Остаток</b>: {sum_income - sum_product}"
    return result


