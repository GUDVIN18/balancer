from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.bot_app.bot_command import start, callback_query
from apps.bot_app.models import TelegramBotConfig
import logging
from apps.stickers.stickers_command import start_stickers

from apps.bot_app.bot_core import tg_bot as bot


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Запск бота кнопки и текст в файле bot_command '

    def handle(self, *args, **options):
        from apps.bot_app.models import BotUser
        # bot = tg_bot

        #handler.py под каждое прложение

        @bot.message_handler(commands=['start'])
        def start_bot(message):
            user, create = BotUser.objects.get_or_create(
                tg_id = message.from_user.id,
                first_name = message.from_user.first_name,
                last_name = message.from_user.last_name,
                username = message.from_user.username,
                language = message.from_user.language_code,
                premium = message.from_user.is_premium
            )
            if user:
                self.stdout.write(self.style.SUCCESS(f'Пользователь получен: {user.tg_id}'))
            if create:
                self.stdout.write(self.style.SUCCESS(f'Пользователь создан: {user.tg_id}'))
            start(bot, message)



        @bot.message_handler(commands=['stickers'])
        def stickers(message):
            # image_path = '/home/dmitriy/SD/face_to_face_server/face_to_face_server_0/face_to_face_server0/media/stickers_photo/image-6.png'
            # mask_path = '/home/dmitriy/SD/face_to_face_server/face_to_face_server_0/face_to_face_server0/media/stickers_photo/Frame 46.png'  
            # apply_mask(image_path, mask_path)
            start_stickers(bot, message)



            


        @bot.callback_query_handler(func=lambda call: True)
        def callback_query_bot(call):
            callback_query(bot, call)
            bot.answer_callback_query(call.id)




        self.stdout.write(self.style.SUCCESS('Starting the bot...'))
        bot.polling(none_stop=True, timeout=120)