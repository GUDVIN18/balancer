from django.db import models
from apps.bot_app.models import BotUser

# class Film(models.Model):
#     film_name = models.CharField(max_length=250, verbose_name="Название фильма", blank=True, null=True)

#     def __str__(self):
#         return f"{self.film_name}"  
      
#     class Meta:
#         verbose_name = "Фильм"
#         verbose_name_plural = "Фильмы"


# class Generate_Stickers(models.Model):
#     user = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='sticker_packs', verbose_name="Пользователь")
#     sticker_set_name = models.CharField(max_length=250, verbose_name="Имя набора стикеров", default='')
#     photo_1 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 1")
#     photo_2 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 2")
#     photo_3 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 3")
#     photo_4 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 4")
#     photo_5 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 5")
#     photo_6 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 6")
#     photo_7 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 7")
#     photo_8 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 8")
#     photo_9 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 9")
#     photo_10 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 10")
#     photo_11 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 11")
#     photo_12 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 12")
#     photo_13 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 13")
#     photo_14 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 14")
#     photo_15 = models.ImageField(upload_to='stickers/', null=True, blank=True, verbose_name="Фото 15")  
#     pack_created = models.BooleanField(default=False, verbose_name="Пак создан?")

#     ready_for_generation = models.BooleanField(null=False, blank=False, default=False, verbose_name="Ready for Gen")

#     def __str__(self):
#         return f"Стикер пак для пользователя {self.user.tg_id}"

#     class Meta:
#         verbose_name = "Созданный стикерпак"
#         verbose_name_plural = "Созданные стикерпаки"


# class Photo_Generate_Stickers(models.Model):
#     target_photo = models.ImageField(upload_to='stickers_photo/', verbose_name='Фото героя', null=True, blank=True)
#     emoji = models.CharField(max_length=5, verbose_name="Эмодзи", blank=True, null=True)

#     def __str__(self):
#         return f"{self.id}"  
      
#     class Meta:
#         verbose_name = "Фото для генерации"
#         verbose_name_plural = "Фото для генерации"

# ___________________________________________________________________________________________________

#Под стикер пак в принципе (для фильма например)

class StikerPackConfig(models.Model):
    pack_name = models.CharField(verbose_name="StikerPack Name")

    main_pack_stiker = models.ImageField(upload_to='main_stickers/', verbose_name='Main sticker', null=True, blank=True)

    def __str__(self):
        return f"{self.pack_name}"


    class Meta:
        verbose_name = "Созданный стикерпак"
        verbose_name_plural = "Созданные стикерпаки"



class Generate_Stickers(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='sticker_packs', verbose_name="Пользователь")
    sticker_set_name = models.CharField(max_length=250, verbose_name="Имя набора стикеров")
    
    pack_created = models.BooleanField(default=False, verbose_name="Пак создан?")

    ready_for_generation = models.BooleanField(null=False, blank=False, default=False, verbose_name="Ready for Gen")

    stiker_pack = models.ForeignKey(to=StikerPackConfig, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Стикер пак")

    def __str__(self):
        return f"Стикерпак №{self.id}"
    class Meta:
        verbose_name = "Пользовательский стикерпак"
        verbose_name_plural = "Пользовательские стикерпаки"






class Stiker_target_photo(models.Model):
    photo_name = models.CharField(verbose_name="Photo name")

    target_photo = models.ImageField(upload_to='stickers_photo/', verbose_name='Фото героя', null=True, blank=True)
    emoji = models.CharField(max_length=5, verbose_name="Эмодзи", blank=True, null=True)
    mask = models.ImageField(upload_to='mask/', verbose_name='Маска героя', null=True, blank=True)
    
    stiker_pack = models.ForeignKey(to=StikerPackConfig, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Стикер пак")

    def __str__(self):
        return f"id {self.id} | Name - {self.photo_name}"

    class Meta:
        verbose_name = "Фото для генерации"
        verbose_name_plural = "Фото для генерации"




class Stiker_output_photo(models.Model):
    output_photo = models.ImageField(upload_to='stickers_photo/', verbose_name='Фото героя', null=True, blank=True)
    emoji = models.CharField(max_length=5, verbose_name="Эмодзи", blank=True, null=True)
    stiker_pack = models.ForeignKey(to=Generate_Stickers, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Стикер пак")
    original_photo_id = models.IntegerField(null=True, blank=True, verbose_name='original_photo_id')

    def __str__(self):
        return f"id {self.id}"

    class Meta:
        verbose_name = "Фото после генерации"
        verbose_name_plural = "Фото после генерации"