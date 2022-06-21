import os
import logging
import transliterate
from transliterate import translit
from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN

#TOKEN = os.getenv('TOKEN')

logging.basicConfig(filename='textsave.txt', 
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)
                    
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f'Hello {user_name}!, nice to meet you! write your name and sur name.'
    logging.info(f"{user_name=} {user_id=} sent message: {message.text}")
    await message.reply(text)

@dp.message_handler(content_types=['text'])
async def send_translation(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text.upper().replace('Ь', '').replace('-', '').replace('Я', 'ИА').replace('Ю', 'ИУ').replace('Ъ', 'ИЕ').replace('Щ', 'ШЧ').replace('Х', 'КХ')
        # ъ -- IE, щ -- SHCH  , х -- KH?


    text = (translit(text, language_code='ru', reversed=True)).upper()
    logging.info(f"{user_name=} {user_id=} sent message: {text}")
    await bot.send_message (message.chat.id, text)

if __name__ == '__main__':
    executor.start_polling(dp)