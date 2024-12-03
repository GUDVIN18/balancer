from django.core.management.base import BaseCommand
import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InputFile, InputSticker
from PIL import Image
from asgiref.sync import sync_to_async
from apps.bot_app.models import TelegramBotConfig
from apps.stickers.models import Generate_Stickers

# class Command(BaseCommand):
#     help = 'Process stickers asynchronously'

#     @sync_to_async
#     def get_bot_token(self):
#         config = TelegramBotConfig.objects.first()
#         if config:
#             return config.bot_token
#         raise ValueError("Bot token not found in database")

#     @sync_to_async
#     def get_sticker_packs(self):
#         return list(Generate_Stickers.objects.all())

#     @sync_to_async
#     def get_user_tg_id(self, sticker_pack):
#         return sticker_pack.user.tg_id

#     @sync_to_async
#     def pack_created_false(self, sticker_pack):
#         sticker_pack.pack_created = False
#         sticker_pack.save()
#         return sticker_pack.pack_created

#     async def resize_image(self, photo_path):
#         with Image.open(photo_path) as img:
#             img.thumbnail((512, 512))
#             img.save(photo_path, "PNG", optimize=True)

#     async def process_stickers(self):
#         bot_token = await self.get_bot_token()
#         bot = AsyncTeleBot(bot_token)

#         while True:
#             sticker_packs = await self.get_sticker_packs()
            
#             for sticker_pack in sticker_packs:
#                 if not sticker_pack.pack_created:
#                     self.stdout.write(f"Sticker pack {sticker_pack.id} not created yet")
#                     continue

#                 if sticker_pack.pack_created:
#                     success = True
#                     photo_fields = [field.name for field in sticker_pack._meta.get_fields() if field.name.startswith('photo_')] #
#                     for field in photo_fields:
#                         photo = getattr(sticker_pack, field)
#                         if photo:
#                             self.stdout.write(f"Processing photo: {photo.path}")
#                             await self.resize_image(photo.path)
#                             try:
#                                 user_tg_id = await self.get_user_tg_id(sticker_pack)
#                                 sticker_added = await bot.add_sticker_to_set(
#                                     user_tg_id,
#                                     sticker_pack.sticker_set_name,
#                                     png_sticker=InputFile(photo.path),
#                                     emojis="👍"
#                                 )
#                                 if not sticker_added:
#                                     success = False
#                                     break
#                             except Exception as e:
#                                 self.stderr.write(f"Error adding sticker: {str(e)}")
#                                 success = False
#                                 break

#                     self.stdout.write('Stickers ready')

#                     user_tg_id = await self.get_user_tg_id(sticker_pack)
#                     if success:
#                         await bot.send_message(user_tg_id, f"Готово! Чтобы добавить стикерпак, нажмите на стикерпак: t.me/addstickers/{sticker_pack.sticker_set_name}")
#                         await self.pack_created_false(sticker_pack)
#                     else:
#                         await bot.send_message(user_tg_id, "Failed to add all stickers to the set.")
#                 else:
#                     user_tg_id = await self.get_user_tg_id(sticker_pack)
#                     await bot.send_message(user_tg_id, "Sticker set was not created.")

#             await asyncio.sleep(1)

#     def handle(self, *args, **options):
#         self.stdout.write('Starting sticker processing...')
#         asyncio.run(self.process_stickers())







class Command(BaseCommand):
    help = 'Process stickers asynchronously'

    # @sync_to_async
    # def get_sticker_packs(self):
    #     return list(Generate_Stickers.objects.all())

    # @sync_to_async
    # def get_user_tg_id(self, sticker_pack):
    #     return sticker_pack.user.tg_id

    # @sync_to_async
    # def pack_created_false(self, sticker_pack):
    #     sticker_pack.pack_created = False
    #     sticker_pack.save()
    #     return sticker_pack.pack_created

    async def resize_image(self, photo_path):
        with Image.open(photo_path) as img:
            img.thumbnail((512, 512))
            img.save(photo_path, "PNG", optimize=True)

    async def process_stickers(self):
        if TelegramBotConfig.objects.exists():
            bot_token = TelegramBotConfig.objects.first()
        else:
            return
        bot = AsyncTeleBot(bot_token)

        while True:
            # sticker_packs = await self.get_sticker_packs()
            sticker_packs = Generate_Stickers.objects.all()
            
            for sticker_pack in sticker_packs:
                if not sticker_pack.pack_created:
                    self.stdout.write(f"Sticker pack {sticker_pack.id} not created yet")
                    continue

                if sticker_pack.pack_created:
                    success = True
                    photo_fields = [field.name for field in sticker_pack._meta.get_fields() if field.name.startswith('photo_')] #
                    # stikers_list = []
                    for field in photo_fields:
                        photo = getattr(sticker_pack, field)
                        if photo:
                            self.stdout.write(f"Processing photo: {photo.path}")
                            await self.resize_image(photo.path)
                            try:
                                # new_stiker = InputSticker(
                                #     sticker=InputFile(photo.path),
                                #     emoji_list=["🎮"]
                                # )
                                # stikers_list.append(
                                #     new_stiker,
                                # )
                                user_tg_id = sticker_pack.user.tg_id
                                sticker_added = await bot.add_sticker_to_set(
                                    user_tg_id,
                                    sticker_pack.sticker_set_name,
                                    png_sticker=InputFile(photo.path),
                                    emojis="👍"
                                )
                                if not sticker_added:
                                    success = False
                                    break
                            except Exception as e:
                                self.stderr.write(f"Error adding sticker: {str(e)}")
                                success = False
                                break

                    self.stdout.write('Stickers ready')

                    user_tg_id = sticker_pack.user.tg_id
                    if success:
                        await bot.send_message(user_tg_id, f"Готово! Чтобы добавить стикерпак, нажмите на стикерпак: t.me/addstickers/{sticker_pack.sticker_set_name}")
                        # await self.pack_created_false(sticker_pack)
                        sticker_pack.pack_created = False
                        sticker_pack.save()
                    else:
                        await bot.send_message(user_tg_id, "Failed to add all stickers to the set.")
                else:
                    user_tg_id = sticker_pack.user.tg_id
                    await bot.send_message(user_tg_id, "Sticker set was not created.")

            await asyncio.sleep(1)

    def handle(self, *args, **options):
        self.stdout.write('Starting sticker processing...')
        asyncio.run(self.process_stickers())
