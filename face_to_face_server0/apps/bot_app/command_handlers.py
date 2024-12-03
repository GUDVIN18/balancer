from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.bot_app.models import TelegramBotConfig, BotUser, GenerationProcess, Images
import threading
from datetime import datetime 
import time
from multiprocessing import Process
import time 
import multiprocessing
import os
from functools import partial
import uuid
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import logging
import traceback

multiprocessing.set_start_method('spawn')


# def handle_send_photo(bot, data_parts, chat_id):
#     data_parts_num = data_parts[1]
#     print(f'---------------{data_parts}---------------')
#     botuser = BotUser.objects.get(tg_id=chat_id)
#     if botuser.generation == False:
#         user_photo = bot.send_message(chat_id=chat_id, 
#             text="Отлично, теперь пришли фото , на котором хорошо видно ваше лицо", 
#         )

        

#         bot.register_next_step_handler(user_photo, partial(get_user_pics, bot, data_parts_num))

#     elif botuser.generation == True:
#         user_photo = bot.send_message(chat_id=chat_id, 
#             text="У вас сейчас есть активная генерация, дождитесь ее окончания и повторите попытку!", 
#         )




from PIL import Image
import io
from telebot.types import InputFile
from functools import partial





def resize_image(bot, file_info):
    downloaded_file = bot.download_file(file_info.file_path)
    
    image = Image.open(io.BytesIO(downloaded_file))
    resized_image = image.resize((512, 512))
    
    img_byte_arr = io.BytesIO()
    resized_image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    # Convert the BytesIO object to bytes
    return img_byte_arr.getvalue()


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
        try:
            logging.info(f'Успешно зашли в функцию get_user_pics\nbot={bot}\ndata_parts_num={data_parts_num}\nmessage={message}\n\n')
            user_id = message.from_user.id
            chat_id = message.chat.id
            botuser = BotUser.objects.get(tg_id=user_id)

        
            file_info = bot.get_file(message.photo[-1].file_id)
            # downloaded_file = bot.download_file(file_info.file_path)
            downloaded_file = resize_image(bot, file_info)
            logging.info('Скачали файл в функции get_user_pics')

            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f'{user_id}_{timestamp}.jpg'

            targ_photo = TargetImages.objects.get(id=int(data_parts_num))
            logging.info(f'targ_photo.target_img {targ_photo.target_img.name}')

            
            c_file = ContentFile(downloaded_file)
            new_generation = GenerationProcess()
            new_generation.user = botuser
            new_generation.target_photo = targ_photo.target_img.name
            new_generation.field_target_id = targ_photo.id
            new_generation.process_status = 'WAITING'
            new_generation.process_backend_id = uuid.uuid4()
            new_generation.photo.save(filename, c_file)
            new_generation.save()
            
            bot.reply_to(message, "Фото успешно получено")
            text = 'ПОЛУЧЕНА НОВАЯ ОБРАБОТКА'
            print(f'\033[92m{text}\033[0m')


            try:
                bot.send_message(chat_id=message.chat.id, 
                        text="Ожидайте обработки", 
                )


                botuser.generation = True
                botuser.save()


            except Exception as e:
                print(f'Ошибка загрузки фото {e}')

        except Exception as e:
            logging.error(f'ОШИБКА get_user_pics {e}')
            logging.error(f'{traceback.format_exc()}')
            
       
    else:
        bot.reply_to(message, "Пожалуйста, отправьте фото.")
        bot.register_next_step_handler(message, partial(get_user_pics, bot, data_parts_num))
        
        


# def run(source_img, target_img):
#     queue = multiprocessing.Queue()
#     source_img = [(f"{source_img}")]
#     p1 = multiprocessing.Process(target=create_generate, args=(source_img, target_img, queue))
#     p1.start()
#     p1.join()
#     print('--> размер', queue.qsize())
#     photo = queue.get()  # Получаем результат из очереди
#     print(f'--- {photo} ---')  # Печатаем результат пути до фото
#     return photo