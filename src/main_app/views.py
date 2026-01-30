import json
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import RegisterForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
# Create your views here.


def index(request):
    return render(request, 'index.html')

# домашняя страница
@login_required(login_url='/login')
def home(request):
    user = request.user
    users_languages = UsersLanguages.objects.filter(user_id=user)
    languages = [ul.language_id for ul in users_languages]
    return render(request, 'main/home.html', {'language': languages})

# выход из аккаунта
@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('/')

# выбор языков
@login_required
def choose_langs(request):
    if request.method == 'POST':
        # Проверяем, пришли ли JSON данные
        
        try:
            data = json.loads(request.body)
            #print(f"JSON данные: {data, request.user.id}")
            for item in data:
                language_id = item.get('language_id')
                if language_id:
                    user_language, created = UsersLanguages.objects.get_or_create(
                        user_id=request.user,
                        language_id=Languages.objects.get(id=language_id)
                    )

            return HttpResponse("Success")
        except json.JSONDecodeError:
            # Если не JSON, пробуем как обычную форму
            pass
    elif request.user:
        Users_Languages = UsersLanguages
        uls = Users_Languages.objects.filter(user_id = request.user)
        langs_id = []
        for user_lang in uls:
            langs_id.append(user_lang.language_id.id)
        languages_list = Languages.objects.exclude(id__in = langs_id) 
        return render(request, 'registration/choose-lang.html', {'languages_list': languages_list})
    else:           
        languages_list = Languages.objects.all()
        return render(request, 'registration/choose-lang.html', {'languages_list': languages_list})
    
    
@login_required
def lang_levels(request, language_name):
    
    user = request.user
    language = Languages.objects.get(language_name=language_name)
    language_exists = UsersLanguages.objects.filter(
            user_id=user,
            language_id__language_name=language_name
        ).exists()
    if not language_exists:
        return redirect('/choose-lang')
    levels = Tasks.objects.filter(
            language__language_name=language_name
        ).values_list('level__level', flat=True).distinct().order_by('level__level')
    
    return render(request, 'main/lang-levels.html', {'levels': levels, 'language': language})
    

    
@login_required
def lang_tasks(request, language_name, level):
    user = request.user
    
    # Проверяем, что пользователь изучает этот язык
    try:
        user_language = UsersLanguages.objects.get(
            user_id=user,
            language_id__language_name=language_name
        )
    except UsersLanguages.DoesNotExist:
        return redirect('/choose-lang')
    
    # Получаем язык и уровень
    language = Languages.objects.get(language_name=language_name)
    
    # Получаем все задания для языка и уровня
    tasks = Tasks.objects.filter(
        language__language_name=language_name,
        level__level=level
    ).order_by('count')
    
    # Получаем прогресс пользователя для этих заданий
    task_ids = tasks.values_list('id', flat=True)
    user_progress = UserProgress.objects.filter(
        user_language=user_language,
        task_id__in=task_ids
    )
    
    # Создаем словарь для быстрого доступа: {task_id: status}
    progress_dict = {progress.task_id: progress.status for progress in user_progress}
    
    # Объединяем задания с их прогрессом
    tasks_with_progress = []
    for task in tasks:
        status = progress_dict.get(task.id, 'not_started')  # по умолчанию 'not_started'
        tasks_with_progress.append({
            'task_id': task.id,
            'task': task.title,
            'status': status,
            'count': task.count,
            'completed': status == 'completed',
            'in_progress': status == 'in_progress',
            'didnt_pass': status == 'didnt_pass',
            'not_started': status == 'not_started',
        })
    
    
    return render(request, 'main/lang-tasks.html', {'tasks_with_progress': tasks_with_progress, 'language': language})
    
@login_required
def btn_progress(request):
    user = request.user
    data = json.loads(request.body)
    level = data.get('level')
    language = data.get('language')
    
    
@login_required
def start_task(request):
    if request.method == 'POST':
        data =json.loads(request.body)
        taskId = data.get('task_id')
        try:
            tasks = Tasks.objects.get(
                id = taskId
            )
            
        except Exception as e:
            return HttpResponse(f'<h1>ERROR: {e}</h1>')
    return render(request, 'main/screen.html', {'tasks':tasks})
    
# регистрация
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/choose-lang')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})



@login_required
def set_progress(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('task_id')
        user = request.user
        mark = data.get('mark')
        count = data.get('count')
        level = data.get('level')
        language = data.get('language')
        
        user_language = UsersLanguages.objects.get(
            user_id=user,
            language_id__language_name = language
        )
        
        UserProgress.objects.update_or_create(
            task_id = task_id,
            user_language = user_language,
            defaults={  # ВСЕ поля для создания/обновления должны быть здесь!
                'status': 'completed',
                'mark': 'correct' in mark
            }
        )
        progress = UserProgress.objects.filter(
                user_language = user_language,
                task__level__level = level
            ).order_by('task__count')
        try:
            new_task = Tasks.objects.get(
                level__level = level,
                count = int(count)+1
            )   
        except Exception:
            new_task = None
            pass
        if new_task:
            return render(request, 'main/screen.html', {'tasks':new_task, 'progress':progress})
        else:

            for p in progress:
                print(f"""
                      Count: {p.task.count}
                      User: {p.user_language.user_id}
                      Task: {p.task.title}
                      status: {p.status}
                      Mark: {p.mark}
                      """)
            return render(request, 'main/screen-info.html', {'progress':progress, 'language':language})
        

        
        