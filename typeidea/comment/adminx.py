from django.contrib import admin
from .models import  Comment

import xadmin
# Register your models here.

@xadmin.sites.register(Comment)
class CommentAdmin():
    list_display = ('target', 'content', 'nickname', 'website', 'created_time')
