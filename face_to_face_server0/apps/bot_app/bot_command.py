from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.bot_app.models import TelegramBotConfig
from apps.bot_app.command_handlers import handle_send_photo
from apps.stickers.stickers_command import photo_to_sticker
import logging



def start(bot, message):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("1", callback_data="photo_1"))
    keyboard.row(InlineKeyboardButton("2", callback_data="photo_2"))
    keyboard.row(InlineKeyboardButton("3", callback_data="photo_3"))

    bot.send_photo(message.chat.id, photo=open('/home/dmitriy/SD/face_to_face_server/face_to_face_server_0/face_to_face_server0/media/main/main_photo.jpg', 'rb'))
    bot.send_message(message.chat.id, "Здравствуйте, выберете фото", reply_markup=keyboard)



def callback_query(bot, call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    data_parts = call.data.split('_')
    data_parts_new_photo = call.data
    print(data_parts)
    
    if data_parts[0] == "photo":
        handle_send_photo(bot, data_parts, chat_id)

    if data_parts[0] == "pack":
        text = '''
Загрузите, пожалуйста, свою фотографию.

<b>Следуйте советам:</b>
— на фото должно быть хорошо видно ваше лицо;
— на фото не должно быть других лиц, кроме вашего;
— желательно без головного убора и очков;
— если вы носите очки, то попробуйте использовать фото без них;
— не отправляйте фото животных, бот распознаёт только лица людей.

Обычно обработка фото занимает до 5 минут. Но при большой очереди придется подождать дольше 🥹
'''
        name_sticer_pak = data_parts[1]
        logging.info(f'name_sticer_pak - {name_sticer_pak}')
        a = bot.send_message(call.message.chat.id, text, parse_mode='HTML')
        bot.register_next_step_handler(a, lambda message: photo_to_sticker(bot, message, name_sticer_pak))

    elif data_parts_new_photo == "new_generate":
        start(bot, call.message)

    else:
        bot.answer_callback_query(call.id, "Неизвестный тип данных")