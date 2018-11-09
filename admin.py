from django.contrib import admin

from .models import Question
from .models import Music,Singer,Listener,Publisher,Mark,UserSongList
admin.site.register(Question)
admin.site.register(Music)
admin.site.register(Singer)
admin.site.register(Listener)
admin.site.register(Publisher)
admin.site.register(Mark)
admin.site.register(UserSongList)
#向管理页面注册了问题 Question 类。Django 知道它应该被显示在索引页