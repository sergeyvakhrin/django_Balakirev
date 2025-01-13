from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
import uuid # уникальные строчки


from women.forms import AddPostForm, UploadFileForm
from women.models import Women, Category, TagPost, UploadFiles

from django.core.mail import send_mail


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

# data_db = [
#     {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h1>Анджелина Джоли</h1> (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
#     Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''',
#      'is_published': True},
#     {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
#     {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
# ]

cats_db =[
    {'id': 1, "name": "Актрисы"},
    {'id': 2, "name": "Певицы"},
    {'id': 3, "name": "Спортсменки"},
]


def index(request):
    data_db = Women.objects.filter(is_published=1).select_related('cat')
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
        'cat_selected': 0
    }
    return render(request, 'women/index.html', context=data)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    data_db = Women.objects.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': data_db,
        'cat_selected': category.pk
    }
    return render(request, 'women/index.html', data)

# def handle_upload_file(f):
#     """ Функция для загрузки файлов на сервер """
#     with open(f"uploads/{uuid.uuid4()}_{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_upload_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1
    }
    return render(request, 'women/post.html', data)


def addpage(request):
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        # try:
        #     Women.objects.create(**form.cleaned_data) # создаем новую запись в базе распаковывая форму
        #     return redirect('home')
        # except:
        #     form.add_error(None, "Ошибка добавления записи")
        if form.is_valid():
            form.save()
        return redirect('home')
    else:
        form = AddPostForm()

    data = {
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form
    }

    return render(request, 'women/addpage.html', data)


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.all().select_related('cat')
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None
    }
    return render(request,'women/index.html', data)
