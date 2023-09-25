from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
# import buttons
 
from config import TOKEN
 
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
 
 
 
def get_result(name):
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute("""DELETE from films
    WHERE   """)
    con.commit()
    con.close()
 
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("ЭТО ХЕЛПЕР")
 
 
#@dp.message_handler()
#async def echo_message(msg: types.Message):
#   await bot.send_message(msg.from_user.id, msg.text)
 
# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="/films"))
    poll_keyboard.add(types.KeyboardButton(text="/other"))
    await message.answer("Это стартовое меню!", reply_markup=poll_keyboard)
 
# Хэндлер на текстовое сообщение с текстом "Фильмы"
@dp.message_handler(commands=["films"])
async def films(message: types.Message):
    # remove_keyboard = types.ReplyKeyboardRemove()
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Драма"))
    poll_keyboard.add(types.KeyboardButton(text="Криминал/Детектив"))
    poll_keyboard.add(types.KeyboardButton(text="3️Фэнтези/Фантастика"))
    poll_keyboard.add(types.KeyboardButton(text="История/Биография"))
    # poll_keyboard.add(types.KeyboardButton(text="5️6️Короткометражка"))
    poll_keyboard.add(types.KeyboardButton(text="Cемейный/Мульт"))
    poll_keyboard.add(types.KeyboardButton(text="Комедия"))
    poll_keyboard.add(types.KeyboardButton(text="Триллер"))
    poll_keyboard.add(types.KeyboardButton(text="Ужасы"))
    poll_keyboard.add(types.KeyboardButton(text="Военный"))
    poll_keyboard.add(types.KeyboardButton(text="/start"))
    await message.answer("Выберите жанр!", reply_markup=poll_keyboard)
 
@dp.message_handler(lambda message: message.text == "Драма")
async def db_search(message: types.Message):
    if message.text == "Драма":
        await message.answer("Робит") # здесь сделать запрос и вывод и так по всем пунктам
 
# Хэндлер на текстовое сообщение с текстом “Отмена”
@dp.message_handler(commands=["other"])
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Введите /start, чтобы попасть в начало."
                         "Вв", reply_markup=remove_keyboard)
 
 
if __name__ == '__main__':
    executor.start_polling(dp)
