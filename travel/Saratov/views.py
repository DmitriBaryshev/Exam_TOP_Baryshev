from django.http import HttpResponse, HttpResponseNotFound, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_GET
from . import forms
from . import models

from django.template.loader import render_to_string


menu = [
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Регистрация", 'url_name': 'register'},
        {'title': "Войти", 'url_name': 'login_p'},
    ]

data_db = [
    {'id': 1, 'title': 'Старый город', 'content': 'Набережная Саратова — улица в Волжском районе города Саратова, протянувшаяся вдоль правого берега Волги от улицы Провиантской до моста Саратов — Энгельс. В 2018 году была признана самой красивой городской набережной в России.', 'is_published': True},
    {'id': 2, 'title': 'Азия', 'content': 'Парк Победы — мемориальный комплекс, посвящённый победе в Великой Отечественной войне, расположенный в Октябрьском районе города Саратова. Открытие состоялось 9 мая 1975 года. Общая площадь парка составляет 8 гектаров.', 'is_published': True},
    {'id': 3, 'title': 'Гастродвор', 'content': 'Проспект Столыпина — одна из центральных магистралей Саратова, проходит через Октябрьский и Фрунзенский районы города. Проспект назван в честь Петра Аркадьевича Столыпина, который был выдающимся государственным деятелем Российской империи начала XX века.', 'is_published': True},
]

cats_db = [
    {'id': 1, 'name': 'Кафе'},
    {'id': 2, 'name': 'Рестораны'},
    {'id': 3, 'name': 'Гостиницы'},
]


def index(request):
    # t = render_to_string('Saratov/index.html')
    # return HttpResponse(t)
    data = {
        'title': 'Саратов',
        'menu': menu,
        'posts': list(models.BlogMessage.objects.all()),
        'cat_selected': 0,
    }
    return render(request, 'Saratov/index.html', context=data)


def about(request):
    return render(request, 'Saratov/about.html', {'title': 'Саратов — город на юго-востоке европейской части России, административный центр Саратовской области. Расположен на правом берегу Волгоградского водохранилища реки Волга. Крупный промышленный, культурный и образовательный центр. Основан в 1590 году. Население — 840 600 человек. Площадь города — 390,3 км².', 'menu': menu})


def categories(request, cat_id):
    return HttpResponse(f"<h1>Страница по категориям</h1><p>id:{cat_id}</p>")


def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Страница по категориям</h1><p>slug:{cat_slug}</p>")


def show_post(request, post_id):
    data = {
        'title': 'Саратов',
        'menu': menu,
        'posts': list(models.BlogMessage.objects.filter(pk=post_id)),
        'cat_selected': 0,
    }
    return render(request, 'Saratov/single.html', context=data)


def contact(request):
    return HttpResponse("https://vk.com/baryshev_64")


def show_category(request, cat_id):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
    }
    return render(request, 'Saratov/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def register(request: HttpRequest):

    # -- GET --
    if request.method == 'GET':
        from_kwargs = {'form': forms.UserFormRegister()}
        return render(request, 'Saratov/register_page.html', from_kwargs)

    # -- POST --
    reg_form = forms.UserFormRegister(request.POST)

    if not reg_form.is_valid():
        return redirect(register)

    username = reg_form.cleaned_data.get('username')
    if models.User.objects.filter(username=username).exists():
        messages.info(request, 'Имя пользователя занято')
        return redirect(register)

    user = reg_form.save()
    user.set_password(reg_form.cleaned_data.get('password'))
    user.save()

    return redirect(login_p)


def login_p(request: HttpRequest):
    # -- GET --
    if request.method == 'GET':
        template_kwargs = { 'form': forms.UserFormLogin() }
        return render(request, 'Saratov/login_page.html', template_kwargs)

    # -- POST --
    login_form = forms.UserFormLogin(request.POST)

    if not login_form.is_valid():
        return redirect( login_p, errors=login_form.errors )

    password = login_form.cleaned_data.get('password')
    username = login_form.cleaned_data.get('username')

    if not models.User.objects.filter(username=username).exists():
        messages.info(request, 'Неверное имя пользователя!')
        return redirect( login_p )

    user = authenticate(request, password=password, username=username)

    if user is None:
        messages.info(request, 'Неверный пароль!')
        return redirect( login_p )

    login(request, user)
    return redirect( index )


def add_blog(request: HttpRequest):
    # -- GET --
    if request.method == 'GET':
        blog_form = forms.BlogForm()
        from_kwargs = {'form': blog_form}
        return render(request, 'Saratov/add_blog.html', from_kwargs)

    # -- POST --
    blog_form = forms.BlogForm(request.POST, sender=request.user)
    if blog_form.is_valid():
        blog_form.save()
        return redirect( index )

    return redirect( add_blog )
