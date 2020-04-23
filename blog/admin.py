from django.contrib import admin
from .models import *




class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'avatar', 'description']


admin.site.register(UserProfile, UserProfileAdmin)


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']
    list_display = ['id', 'title', 'category', 'created_at', 'promoted']


admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'cover']


admin.site.register(Category, CategoryAdmin)