from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Post, Category


def index(request):
    # Получаем все посты, отфильтрованные по критериям публикации
    posts = Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,).order_by('-pub_date')[:5]

    # Подготавливаем контекст для шаблона
    context = {
        'post_list': posts,
    }

    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    # Получаем пост по ID
    post = get_object_or_404(Post, pk=id)

    # Проверяем условие 1: дата публикации не позже текущего времени
    if post.pub_date > timezone.now():
        raise get_object_or_404(Post, pk=None)

    # Проверяем условие 2: пост опубликован
    if not post.is_published:
        raise get_object_or_404(Post, pk=None)

    # Проверяем условие 3: категория опубликована
    if post.category and not post.category.is_published:
        raise get_object_or_404(Post, pk=None)

    # Подготавливаем контекст для шаблона
    context = {
        'post': post,
    }

    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    # Получаем категорию по slug
    category = get_object_or_404(Category, slug=category_slug)

    # Проверяем, что категория опубликована
    if not category.is_published:
        raise get_object_or_404(Category, slug=None)

    # Получаем все опубликованные посты из этой категории
    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now(),).order_by('-pub_date')

    # Подготавливаем контекст для шаблона
    context = {
        'category': category,
        'post_list': posts,
    }

    return render(request, 'blog/category.html', context)


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=profile).order_by('-pub_date')

    paginator = Paginator(post_list, 10)  # по 10 постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'blog/edit_profile.html', {'form': form})
