import json
from django.shortcuts import render, redirect
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
                    UsersLanguages.objects.get_or_create(
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

