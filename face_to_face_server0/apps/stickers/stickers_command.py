from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.bot_app.models import GenerationProcess
from apps.stickers.command_handlers import handle_send_photo
from apps.bot_app.models import BotUser
# from telegram import Update, InputMediaPhoto
import os 
from apps.stickers.models import Generate_Stickers, Stiker_target_photo, StikerPackConfig
from functools import partial
from telebot.types import InputFile
from PIL import Image
import io
import uuid
from django.core.files import File
import time
import logging
from django.core.files.base import ContentFile
from telebot.types import InputFile
from datetime import datetime
import random



def start_stickers(bot, message):
    keyboard = InlineKeyboardMarkup()
    pack_configs = StikerPackConfig.objects.all()
    for pack_config in pack_configs:
        keyboard.row(InlineKeyboardButton(f"{pack_config.pack_name}", callback_data=f"pack_{pack_config.pack_name}"))

    # bot.send_photo(message.chat.id, photo=open('/home/dmitriy/SD/face_to_face/face_to_face/apps/management/commands/main_photo.jpg', 'rb'))
    bot.send_message(message.chat.id, "Здравствуйте, выберете фильм", reply_markup=keyboard)



def get_photo_path(user_id):
    filename = f"photo_{user_id}.png"
    return os.path.join('user_photo', filename)

def photo_to_sticker(bot, message, name_sticer_pak):
    if not message.photo:
        a = bot.reply_to(message, "Пожалуйста, отправьте фотографию.")
        bot.register_next_step_handler(a, lambda message: photo_to_sticker(bot, message))

    if message.photo: 
        try:
            bot.send_message(message.chat.id, 'Фото успешно принято на генерацию, ожидайте...')
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            print('перед sticker_set_name')

            sticker_set_name = create_or_get_sticker_set(bot, message.from_user.id, message.from_user.username, name_sticer_pak)
            user_id = message.from_user.id
            botuser = BotUser.objects.get(tg_id=user_id)

            if sticker_set_name:
                photos = Stiker_target_photo.objects.all()
                for photo in photos:

                    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                    filename = f'{user_id}_{timestamp}.jpg'
                    
                    c_file = ContentFile(downloaded_file)
                    resize_image(c_file)

                    print('-----------------------------------', photo.id)
                    

                    new_generation = GenerationProcess()
                    new_generation.user = botuser
                    new_generation.target_photo = photo.target_photo
                    new_generation.process_status = 'WAITING'
                    new_generation.process_backend_id = uuid.uuid4()
                    new_generation.field_target_id = photo.id
                    new_generation.photo.save(filename, c_file)
                    new_generation.generation_for_sticker_pack = True
                    new_generation.save()
                    new_generation.db_id = new_generation.id
                    new_generation.emoji = photo.emoji
                    new_generation.save()

                    print('Принял у', user_id)



        except Exception as e:
            print(f"Произошла ошибка при обработке фото: {str(e)}")
            bot.reply_to(message, f"Произошла ошибка при обработке фото: {str(e)}")






# Функция для уменьшения изображения
def resize_image(photo_path):
    with Image.open(photo_path) as img:
        img.thumbnail((512, 512))  # Устанавливаем максимальный размер стикера 512x512 пикселей
        img.save(photo_path, "PNG", optimize=True)





def create_or_get_sticker_set(bot, user_id, user_name, name_sticer_pak):
    random_num = random.randrange(1, 99999999999)
    set_name = f"sets_{user_id}_{random_num}_by_{bot.get_me().username}"
    print(set_name)

    try:
        if Generate_Stickers.objects.filter(user__tg_id=user_id).exists():
            sticker_pack = Generate_Stickers.objects.filter(user__tg_id=user_id).first()

            if sticker_pack:
                sticker_pack.delete()
                try:
                    sticker_pack = Generate_Stickers.objects.create(user=BotUser.objects.get(tg_id=user_id), stiker_pack=sticker_pack.stiker_pack, sticker_set_name=set_name, )
                    return set_name                    
                except Exception as e:
                    logging.info(f'Error creating sticker set: {e}')
                    return None
        else:
            pack_config = StikerPackConfig.objects.get(pack_name=name_sticer_pak)
            sticker_pack = Generate_Stickers.objects.create(user=BotUser.objects.get(tg_id=user_id), stiker_pack=pack_config, sticker_set_name=set_name)
            return set_name

    except Exception as e:
        logging.info(f'Ошибка в создании стикерпака {e}')



# import random
# from django.db import IntegrityError

# def create_or_get_sticker_set(bot, user_id, user_name):
#     random_num = random.randrange(1000000000, 99999999999)
#     set_name = f"sets_{user_id}_{random_num}_by_{bot.get_me().username}"
#     print(set_name)

#     try:
#         bot_user = BotUser.objects.get(tg_id=user_id)
#     except BotUser.DoesNotExist:
#         print(f"BotUser with tg_id {user_id} does not exist")
#         return None

#     try:
#         # Try to get existing sticker pack
#         # try:
#             if Generate_Stickers.objects.filter(user__tg_id=user_id).first():
#                 sticker_pack = Generate_Stickers.objects.filter(user__tg_id=user_id).first()
            
#                 if sticker_pack:
#                     # If exists, delete and recreate
#                     sticker_pack.delete()
                
#                     # Create new sticker pack
#                     sticker_pack = Generate_Stickers.objects.create(
#                         user=bot_user,
#                         sticker_set_name=set_name,
#                         stiker_pack=sticker_pack.stiker_pack
#                         # Add other necessary fields here
#                     )

#         # except Exception as e:
#                 return set_name

#     except IntegrityError as e:
#         print(f"IntegrityError: {e}")
#         return None
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         return None