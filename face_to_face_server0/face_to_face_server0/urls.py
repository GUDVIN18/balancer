from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from apps.bot_app.views import get_task_status, finish_task_status, get_task_result, create_task, user_waiting
# from apps.worker_app.views import get_task_status


urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_task_status', get_task_status, name="get_task_status"),
    path('finish_task_status', finish_task_status, name="finish_task_status"),
    path('get_task_result', get_task_result, name="get_task_result"),
    path('create_task', create_task, name="create_task"),
    path('user_waiting', user_waiting, name="user_waiting"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
