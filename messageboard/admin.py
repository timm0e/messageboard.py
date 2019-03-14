from django.contrib import admin

# Register your models here.
from messageboard.models import *

admin.site.register(Board)
admin.site.register(Post)
