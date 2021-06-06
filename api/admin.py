from django.contrib import admin
from django.db import models
from .models import Image,Like,Collection,Follower
# Register your models here.


class ImagesInLine(admin.TabularInline):
    model = Image
    extra = 0

admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Collection)
admin.site.register(Follower)