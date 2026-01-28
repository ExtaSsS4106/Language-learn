from django.contrib import admin
from .models import Languages, LanguageLevel, Courses, Tasks, UserProgress
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
    list_display = ('id', 'level', 'index', 'language')
    list_filter = ('language',)
    search_fields = ('level',)
    ordering = ('language', 'index')

# 3. Courses
@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'index', 'language_level')
    list_filter = ('language_level__language', 'language_level')
    search_fields = ('title',)
    ordering = ('language_level', 'index')
    list_select_related = ('language_level',)

# 4. Tasks
@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'index')
    list_filter = ('course', 'course__language_level')
    search_fields = ('title', 'content')
    ordering = ('course', 'index')
    list_select_related = ('course',)

# 5. UserProgress
@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'get_language', 'task', 'course', 'status', 'started_at', 'updated_at')
    list_filter = ('status', 'course', 'started_at')
    search_fields = ('user_language__user__username', 'task__title', 'course__title')  # ← ИСПРАВЛЕНО
    ordering = ('-updated_at',)
    readonly_fields = ('started_at', 'updated_at')
    list_select_related = ('user_language', 'task', 'course')
    
    # Методы для отображения пользователя и языка
    def get_user(self, obj):
        return obj.user_language.user.username
    get_user.short_description = 'Пользователь'
    get_user.admin_order_field = 'user_language__user__username'
    
    def get_language(self, obj):
        return obj.user_language.language.language_name
    get_language.short_description = 'Язык'
    get_language.admin_order_field = 'user_language__language__language_name'