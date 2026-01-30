from django.db import models
from django.contrib.auth.models import User


# языки
class Languages(models.Model):
    language_name = models.CharField(max_length=255, null=False)
    ico = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.language_name

# Уровни языков
class LanguageLevel(models.Model):
    level = models.CharField(max_length=45, null=False)

    def __str__(self):
        return f"{self.level}"


# задания
class Tasks(models.Model):
    TYPE_CHOICES = [
        ('teory', 'Теория'),     
        ('practic', 'Практика'), 
        ('test', 'Тест'),
        ('none', 'None')        
    ]
    
    count = models.IntegerField(null=False)
    
    # content
    _type = models.CharField(max_length=30,choices=TYPE_CHOICES,default='none',null=False)
    _img = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    content = models.TextField(null=False)
    wrong_answers = models.JSONField(
            default=list,  # значение по умолчанию - пустой список
            null=True,
            blank=True
        )    
    answers = models.TextField(null=True)
    
    
    # connections
    language = models.ForeignKey(Languages, on_delete=models.CASCADE)
    level = models.ForeignKey(LanguageLevel, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} (индекс: {self.id})"


# связь между пользователей и языков
class UsersLanguages(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    language_id = models.ForeignKey(Languages, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return f"Пользователь: {self.user_id.username}, язык: {self.language_id.language_name} "
    

# прогресс пользователей    
class UserProgress(models.Model):
    STATUS_CHOICES = [
        ('didnt_pass', 'Не прошёл'),      # <- КОРТЕЖ (значение, отображение)
        ('in_progress', 'В процессе'),     # <- КОРТЕЖ (значение, отображение)
        ('completed', 'Завершено'),        # <- КОРТЕЖ (значение, отображение)
        ('not_started', 'Не начат')
    ]
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    user_language = models.ForeignKey(UsersLanguages, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='not_started',null=False)
    mark = models.BooleanField(null=False, default=False)
    
    class Meta:
        verbose_name = 'Прогресс пользователя'
        verbose_name_plural = 'Прогресс пользователей'
    
    def __str__(self):
        return f"{self.user_language.user_id.username} - {self.language_level_course_task.task.title} ({self.status}) {self.user_language.language_id.language_name}"
    
