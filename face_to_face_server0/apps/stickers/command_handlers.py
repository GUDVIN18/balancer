from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.bot_app.models import BotUser
# from apps.management.commands.SD_generate import generate
import threading
from datetime import datetime 
import time
from multiprocessing import Process
import time 
import multiprocessing
import os
from functools import partial


def handle_send_photo(bot, data_parts, chat_id):
    data_parts_num = data_parts[1]
    print(f'---------------{data_parts}---------------')
    botuser = BotUser.objects.get(tg_id=chat_id)
    if botuser.generation == False:
        user_photo = bot.send_message(chat_id=chat_id, 
            text="Отлично, теперь пришли фото , на котором хорошо видно ваше лицо", 
        )

        bot.register_next_step_handler(user_photo, partial(get_user_pics, bot, data_parts_num))

    elif botuser.generation == True:
        user_photo = bot.send_message(chat_id=chat_id, 
            text="У вас сейчас есть активная генерация, дождитесь ее окончания и повторите попытку!", 
        )
     


def get_user_pics(bot, data_parts_num, message):
    if message.content_type == 'photo':
        print(f'{message} ___\n')
        user_id = message.from_user.id
        try:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f'{user_id}_{timestamp}.jpg'
            src = '/home/dmitriy/SD/generation_stickers/stickers/apps/media/' + filename

            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            
            bot.reply_to(message, "Фото успешно получено")
            text = 'ПОЛУЧЕНА НОВАЯ ОБРАБОТКА'
            print(f'\033[92m{text}\033[0m')


            bot.send_sticker(chat_id=message.chat.id, sticker=open(src, 'rb'))

        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка при обработке фото: {str(e)}")
    else:
        bot.reply_to(message, "Пожалуйста, отправьте фото.")
        bot.register_next_step_handler(message, partial(get_user_pics, bot, data_parts_num))
        
