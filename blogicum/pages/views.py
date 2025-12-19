from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, TemplateView, DetailView, UpdateView
)
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .forms import (
    UserEditForm, CustomUserCreationForm
)
from blog.models import Post

from utils import paginate_queryset, get_comments

User = get_user_model()


class RulesView(TemplateView):
    template_name = "pages/rules.html"


class AboutView(TemplateView):
    template_name = "pages/about.html"


class RegistrationView(CreateView):
    template_name = "registration/registration_form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("blog:index")


class ProfileView(DetailView):
    template_name = "blog/profile.html"
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = get_comments(Post.objects.filter(author=self.object))
        context["page_obj"] = paginate_queryset(self.request, post_list)
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = "blog/user.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        context = {"username": self.request.user.username}

        return reverse_lazy(
            "profile",
            kwargs=context,
        )

    # def logout_view(request):
    #     logout(request)
    #     return redirect_lazy('home')
    #
    #     def get_object(self, queryset=None):
    #         return self.request.user
    #
    #     def get_success_url(self):
    #         context = {"username": self.request.user.username}
    #         return reverse_lazy(
    #             "profile", kwargs=context
    #         )


def server_error(request):
    return render(
        request,
        "pages/500.html",
        status=500
    )


class LogoutView(TemplateView):
    template_name = "registration/logged_out.html"

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


def csrf_failure(request, reason=""):
    return render(
        request,
        "pages/403csrf.html",
        status=403
    )


def page_not_found(request, exception):
    return render(
        request,
        "pages/404.html",
        status=404
    )
