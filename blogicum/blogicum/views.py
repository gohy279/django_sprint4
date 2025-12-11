from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def page_not_found(request, exception=None):
    return render(
        request,
        'pages/404.html',
        {
            'path': request.path
        },
        status=404
    )


def page_forbidden(request, exception=None):
    return render(
        request,
        'pages/403csrf.html',
        status=403
    )


def server_error(request):
    return render(request, 'pages/500.html', status=500)


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:index')  # или куда нужно после регистрации
    else:
        form = UserCreationForm()
    return render(request, 'auth/registration_form.html', {'form': form})
