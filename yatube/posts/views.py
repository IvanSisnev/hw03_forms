from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm
from .models import Post, Group, User


def index(request):
    """
    Обработать запрос перехода на главную страницу.
    """
    # Шаблон
    template = 'posts/index.html'
    # Записи из БД
    posts: Post = Post.objects.all()

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

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
    # Шаблон
    template = 'posts/group_list.html'
    # Сообщество
    group: Group = get_object_or_404(Group, slug=slug)
    # Записи из БД
    posts: Post = group.posts.all()

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

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

    user = User.objects.get(username=username)

    posts = user.posts.all()

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context: dict = {
        'author': user.get_full_name(),
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

    title = str(post)[:30]

    user = post.author
    total_posts_count = user.posts.count()

    context = {
        'post': post,
        'title': title,
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
    title = 'Добавить запись'
    context = {
        'title': title,
    }
    if request.method == "POST":
        form = PostForm(request.POST)
        context['form'] = form
        if form.is_valid():
            text = form.cleaned_data['text']
            author = User.objects.get(pk=request.user.id)
            group = form.cleaned_data['group']
            Post.objects.create(text=text, author=author, group=group)
            return redirect('posts:profile', username=request.user.username)
        return render(request, template, context)
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

    is_edit = True
    template = 'posts/create_post.html'
    title = 'Редактировать запись'

    context = {
        'is_edit': is_edit,
        'template': template,
        'title': title,
        'post': post,
        'form': form,
    }

    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('posts:post_detail', post_id)
        return redirect('posts:post_edit', post_id)
    return render(request, template, context)
