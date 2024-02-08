import asyncio
import logging
import csv
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        next(reader)  # Пропускаем заголовок
        data = list(reader)
    return data

# Использование функции
data = read_csv_file('sat_world_and_us_history.csv')
random_row = random.choice(data)


touple2 = ('2', 'Сколько нужно сахара?', '2 кг', '3 кг', '4 кг', '5 кг', 'A')


# Записываем последний элемент кортежа в переменную answer
answer = random_row[-1]


# Создаем текст вопроса
text = f"Вопрос №{random_row[0]}\n-------------------\n{random_row[2]}\n-------------------\n"
for i, option in enumerate(random_row[3:-1], start=1):
    text += f"{i}) {option}\n"


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6508845178:AAGPjJ2Z_labjrMlhv8uheVh1H3BRqKvtbo")
# Диспетчер
dp = Dispatcher()

# статистика игрока в баллах
stat = 0


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Начать викторину", callback_data="questions"))
    builder.add(types.InlineKeyboardButton(text="Посмотреть статистику", callback_data="stat"))
    await message.answer("Главное меню", reply_markup=builder.as_markup())


@dp.message(Command("questions"))
async def questions(message: types.Message):
    global random_row
    global answer
    global text
    data = read_csv_file('sat_world_and_us_history.csv')
    random_row = random.choice(data)
    answer = random_row[-1]
    text = f"Вопрос №{random_row[0]}\n-------------------\n{random_row[2]}\n-------------------\n"
    for i, option in enumerate(random_row[3:-1], start=1):
        text += f"{i}) {option}\n"
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="1", callback_data="A"))
    builder.add(types.InlineKeyboardButton(text="2", callback_data="B"))
    builder.add(types.InlineKeyboardButton(text="3", callback_data="C"))
    builder.add(types.InlineKeyboardButton(text="4", callback_data="D"))
    builder.add(types.InlineKeyboardButton(text="5", callback_data="E"))
    builder.add(types.InlineKeyboardButton(text="Выйти", callback_data="stop"))
    await message.answer(text, reply_markup=builder.as_markup())


@dp.message()
async def cmd_stat(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Выйти", callback_data="stop"))
    await message.answer("Вы ответили правильно на: " + str(stat) + " вопросов", reply_markup=builder.as_markup())


@dp.callback_query()
async def check_answer(callback: types.CallbackQuery):
    if callback.data == answer:
        await callback.message.answer("Правильно")
        global stat
        stat += 1
        await questions(callback.message)
    elif callback.data == "stop":
        await cmd_start(callback.message)
    elif callback.data == "start":
        await cmd_start(callback.message)
    elif callback.data == "questions":
        await questions(callback.message)
    elif callback.data == "stat":
        await cmd_stat(callback.message)
    else:
        await callback.message.answer("Неправильно")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())



