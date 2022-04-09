from django.http import HttpResponse


def index(request):
    return HttpResponse('Будущее главной страницы')


def group_posts(request, slug):
    return HttpResponse(f'Группа {slug}, в которых пользователи пишут посты')
