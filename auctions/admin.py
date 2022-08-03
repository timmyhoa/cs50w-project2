from django.contrib import admin
from psutil import users
from .models import *

# Register your models here.

admin.site.register(listing)
admin.site.register(bid)
admin.site.register(User)
admin.site.register(category)