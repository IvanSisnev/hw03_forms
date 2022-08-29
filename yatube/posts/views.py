from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm
from .models import Post, Group, User


def paginate(request, posts):
    """
    Создать из списка записей объект для паджинации.
    """
    paginator = Paginator(posts, settings.PAGE_NUM)

    page_number = request.GET.get('page')

    return paginator.get_page(page_number)


def index(request):
    """
    Обработать запрос перехода на главную страницу.
    """
    template = 'posts/index.html'

    posts: Post = Post.objects.all()

    page_obj = paginate(request, posts)

    context: dict = {
        'posts': posts,
        'date_format': Post.date_format,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """
    Обработать запрос перехода на страницу с записями сообщества.
    """
    template = 'posts/group_list.html'

    group: Group = get_object_or_404(Group, slug=slug)

    posts: Post = group.posts.all()

    page_obj = paginate(request, posts)

    context: dict = {
        'group': group,
        'posts': posts,
        'date_format': Post.date_format,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    """
    Обработать запрос перехода на страницу пользователя.
    """
    template = 'posts/profile.html'

    user: User = get_object_or_404(User, username=username)

    posts = user.posts.all()

    page_obj = paginate(request, posts)

    context: dict = {
        'author': user,
        'posts': posts,
        'date_format': Post.date_format,
        'page_obj': page_obj,

    }
    return render(request, template, context)


def post_detail(request, post_id):
    """
    Обработать запрос перехода на страницу записи.
    """
    template = 'posts/post_detail.html'

    post = get_object_or_404(Post, pk=post_id)

    user = post.author
    total_posts_count = user.posts.count()

    context = {
        'post': post,
        'date_format': Post.date_format,
        'total_posts_count': total_posts_count,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    """
    Обработать запрос создания новой записи.
    """
    template = 'posts/create_post.html'
    context = {}

    form = PostForm(request.POST or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = User.objects.get(pk=request.user.id)
        new_post.save()
        return redirect('posts:profile', username=request.user.username)
    form = PostForm()
    context['form'] = form
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    """
    Обработать запрос редактирования записи.
    """
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        return redirect('posts:post_detail', post_id)

    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)

    is_edit = True
    template = 'posts/create_post.html'

    context = {
        'is_edit': is_edit,
        'template': template,
        'post': post,
        'form': form,
    }

    return render(request, template, context)
