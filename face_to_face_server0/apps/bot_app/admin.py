# Register your models here.
from django.contrib import admin
from .models import *

# admin.site.register(TelegramBotConfig)
# admin.site.register(BotUser)
# admin.site.register(GenerationProcess)
admin.site.register(Images)

@admin.register(TelegramBotConfig)
class TelegramBotConfigAdmin(admin.ModelAdmin):
    fields = [
        "bot_token",
        'is_activ',
    ]
    list_display = (
        "id",
        "bot_token",
        'is_activ',
    )
    list_filter = (
        "bot_token",
        'is_activ',
    )
    search_fields = (
        "bot_token",
    )


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    fields = [
        "tg_id",
        "first_name",
        "last_name",
        "username",
        "language",
        "premium",
        "generation"

    ]
    list_display = (
        "tg_id",
        "first_name",
        "username",
        "generation"
    )
    list_filter = (
        "tg_id",
        "username",
        "generation"

    )
    search_fields = (
        "tg_id",
        "username",
        "id"
    )



@admin.register(GenerationProcess)
class GenerationProcessAdmin(admin.ModelAdmin):
    fields = [
        "process_status",
        "process_backend_id",
        "photo",
        "target_photo",
        'server_int',

    ]
    list_display = (
        'id',
        "process_status",
        'server_int'
    )
    list_filter = (
        "process_status",
        "process_backend_id",

    )
    search_fields = (
        "user",
        "process_backend_id",
        "id"
    )


