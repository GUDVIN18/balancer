from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from apps.bot_app.models import GenerationProcess
from apps.worker_app.models import InswapperConfig


def data_server(server_name, server_address, server_port, 
                server_auth_token, server_max_process,
                process_backend_id, task_id, file_path, target_path,):
    
    print(f'----------{file_path}-----------')

    print(f'----------{target_path}-----------')

    files = {
        "file": (f"image_{process_backend_id}.png", open(file_path, "rb")),
        "target_file": (f"target_image_{process_backend_id}.png", open(target_path, "rb"))
    }

    print(f'files ----------{files}-----------\n\n')
    

    inswapper_config_upscale = InswapperConfig.objects.first().upscale
    inswapper_config_codeformer_fidelity = InswapperConfig.objects.first().codeformer_fidelity

    data = {
        "server_name": server_name,
        "server_address": server_address,
        "server_port": server_port,
        "server_auth_token": server_auth_token,
        "server_max_process": server_max_process,
        # "user_tg_id": user_tg_id,
        "process_backend_id": process_backend_id,
        "inswapper_config_upscale": inswapper_config_upscale,
        "inswapper_config_codeformer_fidelity": inswapper_config_codeformer_fidelity,
        "task_id": task_id,
        # "emoji": emoji,
        # 'original_photo_id': original_photo_id,

    }

    
    server_ip = server_address
    server_port = server_port

    print(server_ip, server_port)
    
    url = f"http://{server_ip}:{server_port}/get_data"
    
    try:
        res = requests.post(url, data=data, files=files)
        print(f"PRINT RES {res.content}\n\n\n")
        return res.content
    except requests.RequestException as e:
        print(f'Данные не переданы > {e}')



