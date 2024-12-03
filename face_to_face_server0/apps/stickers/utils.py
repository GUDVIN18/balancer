from PIL import Image
from telebot.types import InputFile, InputSticker
from apps.stickers.models import StikerPackConfig, Stiker_output_photo, Stiker_target_photo
from apps.bot_app.models import GenerationProcess
import random
from PIL import Image
import numpy as np
import logging

# from apps.bot_app.bot_core import tg_bot as bot
# Мем лицо маска 

from PIL import Image
import os

# def resize_image(photo_path, output_directory):
#     try:
#         with Image.open(photo_path) as img:
#             img.thumbnail((512, 512))
            
#             # Создаем новое имя файла для сохранения измененного изображения
#             base_name = os.path.basename(photo_path)
#             name, ext = os.path.splitext(base_name)
#             new_name = f"{name}_resized.png"
#             new_path = os.path.join(output_directory, new_name)
            
#             img.save(new_path, "PNG", optimize=True)
#         print('-------new_path--------', new_path)
#         return new_path
#     except Exception as e:
#         print('resize_image', e)
#         return photo_path  # Возвращаем оригинальный путь в случае ошибки

# def apply_mask(image_path, mask_path, output_directory):
#     try:
#         # Открываем изображение и маску
#         image = Image.open(image_path).convert('RGBA')
#         mask = Image.open(mask_path).convert('RGBA')
    
#         # Изменяем размер маски, если необходимо
#         if image.size != mask.size:
#             image = image.resize(mask.size, Image.LANCZOS)

#         # Накладываем маску на изображение
#         image.putalpha(mask.getchannel('A'))

#         # Сохраняем результат
#         base_name = os.path.basename(image_path)
#         name, _ = os.path.splitext(base_name)
#         output_name = f"{name}_masked.png"
#         output_path = os.path.join(output_directory, output_name)
        
#         image.save(output_path, 'PNG')
#         output_directoryss = '/home/dmitriy/SD/face_to_face_server/face_to_face_server_0/face_to_face_server0/media/mask_resize/mask/'
#         res = resize_image(output_path, output_directoryss)
#         print('----------------------- apply_mask -----------------------', res)
        
#         return res
    

#     except Exception as e:
#         print('apply_mask error:', e)
#         return None
    



# def get_stikers_list(pack):
#     try:
#         stickers_list = []
#         photos = Stiker_output_photo.objects.filter(stiker_pack=pack)

#         for photo in photos:
#             if photo:
#                 generation_process_obj = GenerationProcess.objects.filter(field_target_id=photo.original_photo_id).order_by('-created_at').first()
#                 target_photo = Stiker_target_photo.objects.get(id=generation_process_obj.field_target_id)
#                 output_directory = '/home/dmitriy/SD/face_to_face_server/face_to_face_server_0/face_to_face_server0/media/mask_resize/resize/'
#                 masked_image_path = apply_mask(photo.output_photo.path, target_photo.mask.path, output_directory)
#                 if masked_image_path:
#                     print('masked_image_path ---------------------', masked_image_path)
#                     try:
#                         new_stiker = InputSticker(
#                             sticker=InputFile(f"{masked_image_path}"),
#                             emoji_list=[f"{photo.emoji}"]
#                         )
#                         stickers_list.append(new_stiker)
#                     except Exception as e:
#                         print('Ошибка при создании стикера', e)
#                 else:
#                     print('Ошибка при наложении маски')

#         return stickers_list
#     except Exception as e:
#         print("Ошибка", e)
#         return None




def resize_image(photo_path, output_directory):
    try:
        with Image.open(photo_path) as img:
            # Сохраняем оригинальный формат
            original_format = img.format

            # Изменяем размер, сохраняя пропорции
            img.thumbnail((512, 512))
            
            # Создаем новое имя файла для сохранения измененного изображения
            base_name = os.path.basename(photo_path)
            name, ext = os.path.splitext(base_name)
            new_name = f"{name}_resized{ext}"
            new_path = os.path.join(output_directory, new_name)
            
            # Убедимся, что директория существует
            os.makedirs(output_directory, exist_ok=True)
            
            # Сохраняем изображение в оригинальном формате
            img.save(new_path, format=original_format)
        
        print('-------new_path--------', new_path)
        return new_path
    except Exception as e:
        print('resize_image error:', e)
        return photo_path  # Возвращаем оригинальный путь в случае ошибки











    

# def apply_mask(image_path, mask_path, output_directory):
#     try:
#         # # Открываем изображение и маску
#         # image = Image.open(image_path).convert('RGBA')
#         # mask = Image.open(mask_path).convert('RGBA')
#         print(mask_path, output_directory)
    
#         # # Изменяем размер маски, если необходимо
#         # if image.size != mask.size:
#         #     mask = mask.resize(image.size, Image.LANCZOS)

#         # # Накладываем маску на изображение
#         # image.putalpha(mask.getchannel('A'))

#         # Сохраняем результат
#         # base_name = os.path.basename(image_path)
#         # name, _ = os.path.splitext(base_name)
#         # output_name = f"{name}_masked.png"
#         # output_path = os.path.join(output_directory, output_name)
        
#         # # Убедимся, что директория существует
#         # os.makedirs(output_directory, exist_ok=True)
        
#         # image.save(output_path, 'PNG')
        
#         output_directory_resize = '/home/dmitriy/SD/face_to_face_server/face_to_face_server_0/face_to_face_server0/media/mask_resize/resize/'
#         res = resize_image(image_path, output_directory_resize)
#         # print('----------------------- apply_mask -----------------------', res)
        
#         return res
#     except Exception as e:
#         print('apply_mask error:', e)
#         return None


def apply_mask(image_path, mask_path, output_directory):
   # Открываем изображение и маску
    image = Image.open(image_path).convert('RGBA')
    mask = Image.open(mask_path).convert('RGBA')

    # Изменяем размер маски, если необходимо
    if image.size != mask.size:
        mask = mask.resize(image.size, Image.LANCZOS)

    # Накладываем маску на изображение
    image.putalpha(mask.getchannel('A'))

    # Сохраняем результат
    base_name = os.path.basename(image_path)
    name, _ = os.path.splitext(base_name)
    output_name = f"{name}_masked.png"
    output_path = os.path.join(output_directory, output_name)
    
    # Убедимся, что директория существует
    os.makedirs(output_directory, exist_ok=True)
    
    image.save(output_path, 'PNG')

    output_resize_path = '/home/dmitriy/SD/face_to_face_server/face_to_face_server_0/face_to_face_server0/media/mask_resize/resize/'

    resized_result = resize_image(output_path, output_resize_path)
    
    return resized_result





def get_stikers_list(pack):
    try:
        stickers_list = []
        photos = Stiker_output_photo.objects.filter(stiker_pack=pack)

        for photo in photos:
            if photo:
                generation_process_obj = GenerationProcess.objects.filter(field_target_id=photo.original_photo_id).order_by('-created_at').first()
                target_photo = Stiker_target_photo.objects.get(id=generation_process_obj.field_target_id)
                output_directory = '/home/dmitriy/SD/face_to_face_server/face_to_face_server_0/face_to_face_server0/media/mask_resize/mask/'
                masked_image_path = apply_mask(photo.output_photo.path, target_photo.mask.path, output_directory)
                if masked_image_path:
                    print('masked_image_path ---------------------', masked_image_path)
                    try:
                        new_stiker = InputSticker(
                            sticker=InputFile(masked_image_path),
                            emoji_list=[f"{photo.emoji}"]
                        )
                        stickers_list.append(new_stiker)
                    except Exception as e:
                        print('Ошибка при создании стикера', e)
                else:
                    print('Ошибка при наложении маски')

        return stickers_list
    except Exception as e:
        print("Ошибка в get_stikers_list:", e)
        return None











def send_stikers_pack(bot, stikers_list, generate_stickers_obj):
    user_id = generate_stickers_obj.user.tg_id
    set_name = generate_stickers_obj.sticker_set_name
    set_title = f"Stickers by Brand Games"
    try:
        success = bot.create_new_sticker_set(
            user_id, 
            set_name,
            set_title,
            stickers=stikers_list,
            sticker_format='static'
        )


        print('success', success)
        if success:
            print(f"Sticker pack created successfully: {set_name}")
            bot.send_message(
                user_id,
                f"Готово! Чтобы добавить стикерпак, нажмите на стикерпак: t.me/addstickers/{set_name}",
            )
            generate_stickers_obj.ready_for_generation = False
            generate_stickers_obj.save()

        else:
            print("Failed to create sticker pack")
    except Exception as e:
        print(f"Error creating sticker pack: {e}")
        success = False