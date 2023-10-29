from django.contrib import admin
from .models import CustomUser, Folder, Entry

admin.site.register(CustomUser)
admin.site.register(Folder)
admin.site.register(Entry)