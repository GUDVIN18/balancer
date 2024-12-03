import asyncio
from telebot.types import InputFile
from PIL import Image
from asgiref.sync import sync_to_async
from apps.bot_app.models import TelegramBotConfig
from apps.bot_app.models import GenerationProcess
from apps.worker_app.models import Server
from apps.stickers.models import Generate_Stickers
from apps.worker_app.views import data_server
from apps.stickers.models import Stiker_target_photo, StikerPackConfig
import uuid
import time

from apps.stickers.utils import get_stikers_list, send_stikers_pack
from apps.bot_app.bot_core import tg_bot as bot


while True:
    if GenerationProcess.objects.filter(process_status='WAITING').exists():
        servers = Server.objects.all()

        if servers:
            for server in servers:
                tasks = GenerationProcess.objects.filter(process_status='WAITING', server_int=None)
                for task in tasks:
                    server_generation = GenerationProcess.objects.filter(server_int=server.id, process_status__in = ['ACCEPTED',])
                    if server_generation.count() < server.server_max_process:
                        task.server_int = server.id
                        task.save()
                        print('балансировщик Принял')
                        data_server(
                            server_name=server.server_name,
                            server_address=server.server_adress,
                            server_port=server.server_port,
                            server_auth_token=server.server_auth_token,
                            server_max_process=server.server_max_process,

                            # user_tg_id=task.user.tg_id,
                            
                            process_backend_id=uuid.uuid4(),
                            task_id = task.id,
                            file_path = task.photo.image.path,
                            target_path = task.target_photo.image.path,
                            # emoji = task.emoji,
                            # db_id = task.db_id,
                            # original_photo_id = task.field_target_id,
                        )
        time.sleep(0.1)
    else:
        time.sleep(0.1)


    # if Generate_Stickers.objects.exists() and Generate_Stickers.objects.filter(ready_for_generation=True).exists():
    #     try:
    #         pack = Generate_Stickers.objects.filter(ready_for_generation=True).first()
    #         stickers_list = get_stikers_list(pack)
    #         print('STICKERS_LIST', stickers_list)
            
    #         send_stikers_pack(bot=bot, stikers_list=stickers_list, generate_stickers_obj=pack)
    #     except Exception as e:
    #         print('Ошибка. WORKER 0 ', e)
        
    # else:
    #     print('Ожидаю STICKERS_LIST\n')
