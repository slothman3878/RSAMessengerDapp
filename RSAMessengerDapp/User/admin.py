from django.contrib import admin

# Register your models here.
from .models import User, Key

admin.site.register(User)
admin.site.register(Key)