from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apps.bot_app.models import *
from apps.stickers.models import Generate_Stickers, StikerPackConfig, Stiker_target_photo, Stiker_output_photo
from apps.bot_app.models import TelegramBotConfig, BotUser, GenerationProcess, Images
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from django.http import HttpResponse
import requests
import json


def get_bot_token():
    config = TelegramBotConfig.objects.first()
    if config:
        return config.bot_token
    raise ValueError("Bot token not found in database")


class Task_Handler():
    def __init__(self) -> None:
        # self.bot = telebot.TeleBot(get_bot_token())
        pass

    def sticker(self, task):
        
        if task.generation_for_sticker_pack:
            print("-----------------В создании стикер пака-----------------")
            sticker = Generate_Stickers.objects.filter(user__tg_id=user_id).first()
            if sticker:
                stiker_pack_obj = sticker.stiker_pack

                photos = Stiker_target_photo.objects.filter(stiker_pack=stiker_pack_obj)
                total_photos = len(photos)

                a = Stiker_output_photo.objects.filter(stiker_pack=sticker)

                done_photos = len(a)

                print('ПРОВЕРКА НА КОЛ-ВО ФОТО', total_photos, 'done_photos', done_photos)

                stiker_output_photo = Stiker_output_photo()
                stiker_output_photo.emoji = emoji
                stiker_output_photo.stiker_pack = sticker
                stiker_output_photo.original_photo_id = original_photo_id
                stiker_output_photo.output_photo.save(f'saved/{file.name}', file)
                stiker_output_photo.save()


                print('Успешно создали фото')

                # Проверяем, если текущий элемент - последний в списке
                if total_photos == done_photos + 1:
                    print('--------------- TRUE')
                    sticker.ready_for_generation = True
                    sticker.pack_created = True
                    sticker.save()
                    
                        
                
                else:
                    print("Все поля для фото уже заполнены")
                

            else:
                print("Стикерпак для данного пользователя не найден")  



    def task_end_alert(self, task):
        url = "http://141.105.71.236:8001/api/task_complete_alert/"


        data = {
            "id": task.id,
            "task_status": task.process_status
        }
        
        # Отправка данных как JSON
        response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        
        print('--------- task_end_alert', response)




    def faceswap(self, task):
        if task.generation_for_sticker_pack is not True:  
            bot = self.bot
            botuser = BotUser.objects.get(tg_id=user_id)
            botuser.generation = False
            botuser.save()

            keyboard = InlineKeyboardMarkup()
            keyboard.row(InlineKeyboardButton("Новая генерация", callback_data="new_generate"))
            bot.send_photo(user_id, photo=open(f'{src}', 'rb'), reply_markup=keyboard)
