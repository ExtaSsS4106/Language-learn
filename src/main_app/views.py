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
            'completed': status == 'completed',
            'in_progress': status == 'in_progress',
            'didnt_pass': status == 'didnt_pass',
            'not_started': status == 'not_started',
        })
    
    
    
    return render(request, 'main/lang-tasks.html', {'tasks_with_progress': tasks_with_progress, 'language': language})
    
@login_required
def start_task(request):
    if request.method == 'POST':
        data =json.loads(request.body)
        taskId = data.get('task_id')
        user = request.user
        try:
            tasks = Tasks.objects.get(
                id = taskId
            )
            
            data = {
                'count': tasks.count,
                '_type': tasks._type,
                '_img': tasks._img,
                'title': tasks.title,
                'description': tasks.description,
                'content': tasks.content,
                'wrong_answers': tasks.wrong_answers,
                'answer': tasks.answers,
                'language': tasks.language,
                'level': tasks.level
            }
        except Exception as e:
            return HttpResponse(f'<h1>ERROR: {e}</h1>')
    return render(request, 'main/screen.html', {'data':data})
    
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
def check_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('task_id')
        user = request.user
        status = data.get('status')
        
        match status:
            case 'in_progress':
                UserProgress.objects.update_or_create(
                    task = task_id,
                    user_language = user,
                    status = 'in_progress'
                )
            case 'completed':
                UserProgress.objects.update_or_create(
                    task = task_id,
                    user_language = user,
                    status = 'completed'
                )
            case 'didnt_pass':
                UserProgress.objects.update_or_create(
                    task = task_id,
                    user_language = user,
                    status = 'didnt_pass'
                )
        
        