from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apps.bot_app.models import GenerationProcess, TelegramBotConfig, BotUser, Images
from apps.stickers.models import Generate_Stickers, StikerPackConfig, Stiker_target_photo, Stiker_output_photo
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from apps.bot_app.task_end_handlers import Task_Handler
from django.http import HttpResponse, JsonResponse
from django.core.files.base import ContentFile
import uuid





from django.http import FileResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
import os

from django.http import FileResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404


absolute_path = '/home/dmitriy/SD/face_to_face_server/face_to_face_server_0/face_to_face_server0/media/success'
@csrf_exempt 
def get_task_status(request):
    if request.method == "POST":
        try:
            task_id = int(request.POST.get("id"))
            task_status = request.POST.get("task_status")
        except:
            return HttpResponse("Данные не переданы")
        
        try:
            task = GenerationProcess.objects.get(id=task_id)
            task.process_status = task_status
            task.save()

        except GenerationProcess.DoesNotExist:
            # Обработка ситуации, когда объект не найден
            print(f"GenerationProcess с id={task_id} не существует")

        print(f'________________________{task_status} {task_id}________________________\n\n')
        return HttpResponse("Success")
    else:
        return HttpResponse("Not POST")




@csrf_exempt 
def finish_task_status(request):
    if request.method == "POST":
        print("-----ВХОД ВЫПОЛНЕН---------")
        try:
            task_id = int(request.POST.get("id"))
            task_status = request.POST.get("task_status")
        except:
            return HttpResponse("Данные не переданы")
        
        try:
            task = GenerationProcess.objects.get(id=task_id)
            task.process_status = task_status
            task.save()

        except GenerationProcess.DoesNotExist:
            # Обработка ситуации, когда объект не найден
            print(f"GenerationProcess с id={task_id} не существует")

        # user_id = int(request.POST.get("user_id"))
        # emoji = request.POST.get("emoji")
        # original_photo_id = request.POST.get("original_photo_id")
        task_end_handler = task.task_end_handler
        try:
            file = request.FILES.get("file")
            src = f"{absolute_path}/{file.name}"

            try:
                output_image = Images.objects.create(
                    description = 'Полученное фото после генерации',
                    image = file,
                )
            
                task.output_photo = output_image
                task.save()
            except:
                print('Ошибка при создании Images')
            
            print(f'________________________{task_status} {task_id}________________________\n\n')
            "Тут вызов функций"
            print('finish_task_status')
            if task_end_handler:
                handler = getattr(Task_Handler(), task_end_handler)
                handler(task=task)
            return HttpResponse('OK')
        
        except Exception as e:
            if task_end_handler:
                handler = getattr(Task_Handler(), task_end_handler)
                handler(task=task)
            print('Файл не был передан', e)
            return HttpResponse('Not OK')



            

    else:
        return HttpResponse("Not POST")
    

@csrf_exempt 
def create_task(request):
    if request.method == "POST":
        try:
            target_photo_file = request.FILES.get("target_photo") #Фото обезьяны 
            user_photo_file = request.FILES.get("user_photo") #Фото пользователя
            task_end_handler = request.POST.get("task_end_handler")

        except (ValueError, TypeError):
            return JsonResponse({"error": "Неверный формат данных"}, status=400)
        
        try:

            #Получаем, сколько пользователей перед пользователем
            user_waiting = GenerationProcess.objects.filter(process_status='WAITING').count()
            print(f'\n ---- ПОЛЬЗОВАТЕЛЕЙ В ОЧЕРЕДИ ПЕРЕД НОВОЙ ГЕНЕРЦИЕЙ {user_waiting}\n')
            
            target_photo = Images.objects.create(
                description = 'Фото на которое меняется лицо',
                image=target_photo_file,
                )
            
            user_photo = Images.objects.create(
                description = 'Фото пользователя',
                image=user_photo_file,
            )

            new_generation = GenerationProcess(
                target_photo=target_photo,
                photo = user_photo,
                process_status='WAITING',
                process_backend_id=uuid.uuid4(),
                task_end_handler = task_end_handler,
            )
            
            new_generation.save()
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
        print(f'________________________{new_generation.process_status} {new_generation.id}________________________\n\n')
        return JsonResponse({"task_id": new_generation.id, "status": new_generation.process_status, "user_waiting": user_waiting})
    else:
        return JsonResponse({"error": "Метод не разрешен"}, status=405)

@csrf_exempt
@require_http_methods(["GET"])
def user_waiting(request):
    #Принятых генераций
    procces_accepted = GenerationProcess.objects.filter(process_status='ACCEPTED').count()
    #Завершенных генераций
    proccess_completed = GenerationProcess.objects.filter(process_status='COMPLETED').count()
    #Генераций с ошибкой ERROR_GENERATION
    proccess_error = GenerationProcess.objects.filter(process_status='ERROR_GENERATION').count()

    user_waiting = GenerationProcess.objects.filter(process_status='WAITING').count()

    return JsonResponse({"user_waiting": user_waiting, "procces_accepted": procces_accepted, 
                         "proccess_completed" :proccess_completed, "proccess_error" :proccess_error, })


    

@csrf_exempt
@require_http_methods(["GET"])
def get_task_result(request):
    print('Зашли в get_task_result')
    # Получаем идентификатор задачи из запроса
    task_id = request.GET.get('task_id')
    print(task_id)
    if not task_id:
        print('Не указан идентификатор задачи')
        return HttpResponse("Не указан идентификатор задачи", status=400)
    
    # Получаем объект Task или возвращаем 404, если не найден
    try:
        generation_object = GenerationProcess.objects.get(
            id=int(task_id),
        )
    except Exception as e:
        print('GenerationProcess не найден')
        return HttpResponse("GenerationProcess не найден", status=404)
    
    # Проверяем, есть ли изображение в задаче
    if not generation_object.output_photo:
        print('Изображение не найдено для данной задачи')
        return HttpResponse("Изображение не найдено для данной задачи", status=404)
    
    # Открываем файл изображения
    try:
        file = generation_object.output_photo.image.open()
    except IOError:
        print('Ошибка при открытии файла')
        return HttpResponse("Ошибка при открытии файла", status=500)
    
    # Определяем тип содержимого на основе расширения файла
    file_name = generation_object.output_photo.image.path
    content_type = 'image/jpeg' if file_name.lower().endswith(('.jpg', '.jpeg')) else 'image/png'
    
    # Создаем FileResponse
    response = FileResponse(file)
    response['Content-Type'] = content_type
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    print('ВСЕ ОК')
    
    return response