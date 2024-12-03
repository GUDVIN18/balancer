from django.db import models

class TelegramBotConfig(models.Model):
    bot_token = models.CharField(max_length=100)

    is_activ = models.BooleanField(null=False, blank=False, default=False, verbose_name="Is active")

    def __str__(self):
        return f'{self.bot_token}'

    class Meta:
        verbose_name = "Токен"
        verbose_name_plural = "Токены"


class BotUser(models.Model):
    tg_id = models.BigIntegerField(unique=True, verbose_name="ID Telegram")
    first_name = models.CharField(max_length=250, verbose_name="Имя пользователя", blank=True, null=True)
    last_name = models.CharField(max_length=250, verbose_name="Фамилия пользователя", blank=True, null=True)
    username = models.CharField(max_length=250, verbose_name="Username пользователя", blank=True, null=True)
    language = models.CharField(max_length=250, verbose_name="Язык пользователя", blank=True, null=True)
    premium = models.BooleanField(verbose_name="Имеет ли пользователь премиум-аккаунт", default=False, blank=True, null=True)
    generation = models.BooleanField(default=False, verbose_name="Выполняется ли генерация?")

    def __str__(self):
        return f"{self.tg_id}"

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"





class Images(models.Model):
    description = models.CharField(max_length=255, default=None, blank=True, null=True)
    image = models.ImageField(upload_to='img_storage/', verbose_name='Хранилище фоток', null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
    
    class Meta:
            verbose_name = "Исходник"
            verbose_name_plural = "Исходники"








class GenerationProcess(models.Model):
    PROCESS_STATUS_CHOICES = [
        ('ACCEPTED', 'Процесс принят сервером на генерацию'),
        ('COMPLETED', 'Генерация успешно завершена'),
        ('WAITING', 'Генерация ожидает принятия сервером'),
        ('ERROR_GENERATION', 'Ошибка генерации'),
    ]

    process_status = models.CharField(max_length=110, choices=PROCESS_STATUS_CHOICES)
    process_backend_id = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    photo = models.ForeignKey(to=Images, verbose_name='Загруженное изображение', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT, related_name='photo')
    target_photo = models.ForeignKey(to=Images, verbose_name='На кого будет наложено', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT, related_name='target_photo')
    output_photo = models.ForeignKey(to=Images, verbose_name='Полученное фото после генерации', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT, related_name='output_photo')
    server_int = models.IntegerField(default=None, null=True, blank=True)

    time_completed = models.DateTimeField(default=None, null=True, blank=True)
    task_end_handler = models.CharField(max_length=255, null=True, blank=True, verbose_name='Хендлер завершения таска')
    
    class Meta:
        verbose_name = "Созданный процесс"
        verbose_name_plural = "Созданные процессы"

    def __str__(self):
        return f"Process {self.process_backend_id} - {self.get_process_status_display()}"
    






