import datetime

import django.contrib.auth as auth
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.views import LoginView, SuccessURLAllowedHostsMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.http import is_safe_url
from django.utils.timezone import now
from django.views.generic import DetailView, TemplateView, FormView

from messageboard import forms
from messageboard.models import Board
from messageboard.forms import LoginForm, NewPostForm


class HomeView(TemplateView):
    template_name = "_basepage.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['title'] = "Home"
        return context


class BoardView(TemplateView):
    template_name = 'boardview.html'

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data()
        board = get_object_or_404(Board, pk=self.kwargs['pk'])
        context['board'] = board
        context['title'] = board.name
        posts = [post for post in board.posts.all()]
        context['posts'] = posts
        return context


class NewPost(FormView, LoginRequiredMixin):
    template_name = 'newpost.html'
    form_class = NewPostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        board = get_object_or_404(Board, pk=self.kwargs['pk'])
        context['board'] = board
        context['title'] = board.name
        return context

    def form_valid(self, form):
        form.clean()
        post = form.save(commit=False)
        post.date = now
        post.user = self.request.user
        board = get_object_or_404(Board, pk=self.kwargs['pk'])
        post.board = board
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("boardview", args=[self.kwargs['pk']])


class LoginSignupView(FormView, SuccessURLAllowedHostsMixin):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = auth.authenticate(self.request, username=form.cleaned_data['username'],
                                 password=form.cleaned_data['password'])
        if user is not None:
            auth.login(self.request, user)
            return super().form_valid(form)
        if User.objects.filter(username=form.cleaned_data['username']).exists():
            form.add_error('username', "User already exists")
            form.add_error('password', "Wrong password")
            return super().form_invalid(form)

        user = User.objects.create_user(form.cleaned_data['username'], password=form.cleaned_data['password'])
        auth.login(self.request, user)
        messages.success(self.request, "New account created!")
        return super().form_valid(form)

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or '/'

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            'next',
            self.request.GET.get('next', '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

class NewBoardView(FormView, LoginRequiredMixin):
    form_class = forms.NewBoardForm
    template_name = "newboard.html"
    extra_context = {"title": "Create new board"}

    def form_valid(self, form):
        board = form.save(commit=True)
        return HttpResponseRedirect(reverse("boardview", args=[board.pk]))



