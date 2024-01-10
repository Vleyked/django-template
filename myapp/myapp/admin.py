from django.contrib import admin
from .models import Dinosaur, DinoImage, Favorite


class DinosaurAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "period",
        "size",
        "eating",
        "color",
        "description",
        "created_at",
        "updated_at",
    )


class DinoImageAdmin(admin.ModelAdmin):
    list_display = ("dinosaur", "image")


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "dinosaur")


admin.site.register(Dinosaur, DinosaurAdmin)
admin.site.register(DinoImage, DinoImageAdmin)
admin.site.register(Favorite, FavoriteAdmin)
