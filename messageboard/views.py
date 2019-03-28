import datetime

import django.contrib.auth as auth
import guardian.shortcuts as guardian
from django.contrib import messages
from guardian.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.views import LoginView, SuccessURLAllowedHostsMixin
from django.forms import Form
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.http import is_safe_url
from django.utils.timezone import now
from django.views.generic import DetailView, TemplateView, FormView

from djangotest import settings
from messageboard import forms
from messageboard.models import Board, Post
from messageboard.forms import LoginForm, NewPostForm


class BoardView(TemplateView):
    template_name = 'boardview.html'

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data()
        board = get_object_or_404(Board, pk=self.kwargs['pk'])
        context['board'] = board
        context['title'] = board.name
        posts = [post for post in board.posts.all()]
        posts.reverse()
        context['posts'] = posts
        return context


class NewPost(LoginRequiredMixin, FormView):
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
        guardian.assign_perm("delete_this_post", self.request.user, post)
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
            auth.login(self.request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
            return super().form_valid(form)
        if User.objects.filter(username=form.cleaned_data['username']).exists():
            form.add_error('username', "User already exists")
            form.add_error('password', "Wrong password")
            return super().form_invalid(form)

        user = User.objects.create_user(form.cleaned_data['username'], password=form.cleaned_data['password'])
        auth.login(self.request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
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


class NewBoardView(LoginRequiredMixin, FormView):
    form_class = forms.NewBoardForm
    template_name = "newboard.html"
    extra_context = {"title": "Create new board"}

    def form_valid(self, form):
        board = form.save(commit=True)
        guardian.assign_perm("delete_this_board", self.request.user, board)
        return HttpResponseRedirect(reverse("boardview", args=[board.pk]))


class DeletePostView(LoginRequiredMixin, FormView):
    form_class = Form
    template_name = "deletepost.html"
    extra_context = {"title": "Delete post"}

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.request.user.has_perm("delete_this_post", post):
            post.delete()
            messages.success(self.request, "Your post has been deleted!")
        else:
            messages.error(self.request, "You have no permission to delete this post!")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("posts")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class UserPostsView(LoginRequiredMixin, TemplateView):
    template_name = "userposts.html"

    def get_context_data(self, **kwargs):
        context = super(UserPostsView, self).get_context_data(**kwargs)
        context['title'] = self.request.user.username
        posts = [post for post in self.request.user.posts.all()]
        posts.reverse()
        context['posts'] = posts
        return context


class DeleteBoardView(LoginRequiredMixin, FormView):
    form_class = Form
    template_name = "deleteboard.html"
    extra_context = {"title": "Delete board"}

    def get_context_data(self, **kwargs):
        context = super(DeleteBoardView, self).get_context_data(**kwargs)
        board = get_object_or_404(Board, pk=self.kwargs['pk'])
        context['board'] = board
        return context

    def form_valid(self, form):
        board = get_object_or_404(Board, pk=self.kwargs['pk'])
        if self.request.user.has_perm("delete_this_board", board):
            board.delete()
            messages.success(self.request, "The board has been deleted!")
        else:
            messages.error(self.request, "You have no permission to delete this board!")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("home")

