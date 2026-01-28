from django.db import models
from django.contrib.auth.models import User

"""class Users(AbstractUser):
    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username"""

class Languages(models.Model):
    language_name = models.CharField(max_length=255, null=False)
    ico = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.language_name

class LanguageLevel(models.Model):
    level = models.CharField(max_length=45, null=False)
    index = models.IntegerField(null=False)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.level} (индекс: {self.index} язык: {self.language.language_name})"

class Courses(models.Model):
    title = models.CharField(max_length=255, null=False)
    index = models.IntegerField(null=False)
    language_level = models.ForeignKey(LanguageLevel, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return f"{self.title} (индекс: {self.index} язык: {self.language_level.language.language_name})"

class Tasks(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, null=False)
    content = models.TextField(null=False)
    index = models.IntegerField(null=False)
    wrong_answers = models.TextField(null=False)
    answers = models.TextField(null=False)
    
    def __str__(self):
        return f"{self.title} (индекс: {self.index} язык: {self.course.language_level.language.language_name})"



class UsersLanguages(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    language_id = models.ForeignKey(Languages, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return f"Пользователь: {self.user_id.username}, язык: {self.language_id.language_name} "
    



class UserProgress(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Не начато'),      # <- КОРТЕЖ (значение, отображение)
        ('in_progress', 'В процессе'),     # <- КОРТЕЖ (значение, отображение)
        ('completed', 'Завершено'),        # <- КОРТЕЖ (значение, отображение)
    ]
    
    user_language = models.ForeignKey(UsersLanguages, on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='not_started',
        null=False
    )
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Прогресс пользователя'
        verbose_name_plural = 'Прогресс пользователей'
        unique_together = ['user_language', 'task']
    
    def __str__(self):
        return f"{self.user_language.user_id.username} - {self.task.title} ({self.status}) {self.user_language.language_id.language_name}"
    
