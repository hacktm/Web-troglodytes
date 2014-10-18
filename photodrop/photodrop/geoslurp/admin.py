from django.contrib import admin
from . import models

class PhotoAdmin(admin.ModelAdmin):
    fields = ['title', 'image', 'description']

admin.site.register(models.Photo, PhotoAdmin)

