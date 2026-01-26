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
    
    def __str__(self):
        return self.language_name

class LanguageLevel(models.Model):
    level = models.CharField(max_length=45, null=False)
    index = models.IntegerField(null=False)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.level} (индекс: {self.index})"

class Courses(models.Model):
    title = models.CharField(max_length=255, null=False)
    index = models.IntegerField(null=False)
    language_level = models.ForeignKey(LanguageLevel, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.title

class Tasks(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, null=False)
    content = models.TextField(null=False)
    index = models.IntegerField(null=False)
    wrong_answers = models.TextField(null=False)
    answers = models.TextField(null=False)
    
    def __str__(self):
        return self.title

class UserProgress(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Не начато'),      # <- КОРТЕЖ (значение, отображение)
        ('in_progress', 'В процессе'),     # <- КОРТЕЖ (значение, отображение)
        ('completed', 'Завершено'),        # <- КОРТЕЖ (значение, отображение)
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
        unique_together = ['user', 'task']
    
    def __str__(self):
        return f"{self.user.username} - {self.task.title} ({self.get_status_display()})"