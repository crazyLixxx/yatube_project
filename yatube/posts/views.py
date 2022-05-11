from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from .models import Post, Group

User = get_user_model()


def posts_on_page(request, posts):
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts_on_page = paginator.get_page(page)
    return posts_on_page


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    context = {
        'posts_on_page': posts_on_page(request, posts),
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    context = {
        'group': group,
        'posts_on_page': posts_on_page(request, posts),
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    context = {
        'user': user,
        'posts_on_page': posts_on_page(request, posts),
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, template, context)
