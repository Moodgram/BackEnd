from django.contrib import admin
from .models import User, Diary, DiaryImage, Comment, Like, Friendship, AIAnalysis

admin.site.register(User)
admin.site.register(Diary)
admin.site.register(DiaryImage)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Friendship)
admin.site.register(AIAnalysis)
