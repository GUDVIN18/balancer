from django.db import models


class Server(models.Model):
    server_name = models.CharField(max_length=255, verbose_name="Какое-то произвольное имя сервера")
    server_adress = models.CharField(max_length=255, verbose_name="IP или URL адрес сервера")
    server_port = models.IntegerField(verbose_name="Порт, на который необходимо стучаться")
    server_auth_token = models.CharField(max_length=255, verbose_name="Уникальный токен сервера")
    server_max_process = models.IntegerField(verbose_name="Максимальное кол-во процессов генерации на сервере")
    last_rec_date = models.DateTimeField(verbose_name="Дата последнего запроса на сервер", default='')

    def __str__(self):
        return self.server_name

    class Meta:
        verbose_name = "Сервер"
        verbose_name_plural = "Сервера"



class InswapperConfig(models.Model):
    upscale = models.IntegerField(verbose_name="upscale", help_text="default=8")
    codeformer_fidelity = models.FloatField(verbose_name="codeformer_fidelity", help_text="default=0.90")

    def __str__(self):
        return f"{self.id}"
    
    class Meta:
        verbose_name = "Inswapper config"
        verbose_name_plural = "Inswapper configs"