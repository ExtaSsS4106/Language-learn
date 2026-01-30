from django.contrib import admin

from .models import *
# Register your models here.
# 1. Languages
@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'language_name')
    search_fields = ('language_name',)
    ordering = ('language_name',)

# 2. LanguageLevel
@admin.register(LanguageLevel)
class LanguageLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'level')
    list_filter = ('level',)
    search_fields = ('level',)


# 3. Tasks
@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'count' ,'_type', '_img', 'title', 'description' ,'content', 'wrong_answers', 'answers', 'language', 'level')
    list_filter = ('title',)
    search_fields = ('title', '_type')
    ordering = ('language',)

# 4. UserProgress
@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'task', 'status')
    list_filter = ('status',)
    search_fields = ('user_language__user__username',)  # ← ИСПРАВЛЕНО
    ordering = ('-id',)
    list_select_related = (
        'user_language',
    )
    # Методы для отображения пользователя и языка
    def get_user(self, obj):
        return obj.user_language.user.username
    get_user.short_description = 'Пользователь'
    get_user.admin_order_field = 'user_language__user__username'
    