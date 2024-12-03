from django.contrib import admin

from django.contrib import admin
from apps.stickers.models import Generate_Stickers, StikerPackConfig, Stiker_target_photo, Stiker_output_photo

# @admin.register(Film)
# class FilmAdmin(admin.ModelAdmin):
#     fields = [
#         "film_name",
#     ]
#     list_display = (
#         "id",
#         "film_name",
#     )
#     list_filter = (
#         "film_name",
#     )
#     search_fields = (
#         "film_name",
#     )




class Stiker_output_photoTabularInline(admin.TabularInline):
    model = Stiker_output_photo

@admin.register(Stiker_output_photo)
class Stiker_output_photoAdmin(admin.ModelAdmin):
    fields = [
        "output_photo",
        "emoji",
        "stiker_pack",
        "original_photo_id",
    ]
    list_display = (
        "id",
        "output_photo",
        "emoji",
        "stiker_pack"
    )
    list_filter = (
        "id",
        "stiker_pack",
    )
    search_fields = (
        "id",
        "stiker_pack",
    )



@admin.register(Generate_Stickers)
class Generate_StickersAdmin(admin.ModelAdmin):

    inlines = [Stiker_output_photoTabularInline]
    fields = [
        "user",
        "sticker_set_name",
        "pack_created",
        "ready_for_generation",
        'stiker_pack',
        

    ]
    list_display = (
        "id",
        "user",
        "sticker_set_name",
        "pack_created",
    )
    list_filter = (
        "user",
    )
    search_fields = (
        "user",
        "sticker_set_name",
    )

@admin.register(Stiker_target_photo)
class Stiker_target_photoAdmin(admin.ModelAdmin):
    fields = [
        "photo_name",
        "target_photo",
        'mask',
        "emoji",
        "stiker_pack",
    ]
    list_display = (
        "id",
        "photo_name",
        "target_photo",
        "emoji",
        "stiker_pack"
    )
    list_filter = (
        "id",
        "stiker_pack",
    )
    search_fields = (
        "id",
        "stiker_pack",
    )





class StickerPackConfifTabularInline(admin.TabularInline):
    model = Stiker_target_photo


@admin.register(StikerPackConfig)
class StikerPackConfigAdmin(admin.ModelAdmin):
    inlines = [StickerPackConfifTabularInline]

    fields = [
        "pack_name",
        "main_pack_stiker",
    ]
    list_display = (
        "id",
        "pack_name",
        "main_pack_stiker",

    )
    list_filter = (
        "id",
        "pack_name",
    )
    search_fields = (
        "id",
        "pack_name",
    )






