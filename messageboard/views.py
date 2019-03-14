from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.views.generic import DetailView, TemplateView

from messageboard.models import Board


class HomeView(TemplateView):
    template_name = "_basepage.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['title'] = "Home"
        return context


class BoardView(TemplateView):
    template_name = 'boardview.html'

    def get_context_data(self, **kwargs):
        messages.success(self.request, "Messages work!")
        context = super(BoardView, self).get_context_data()
        board = get_object_or_404(Board, pk=kwargs['pk'])
        context['board'] = board
        posts = [post for post in board.posts.all()]
        context['posts'] = posts
        return context


class NewPost(LoginRequiredMixin, DetailView):
    template_name = 'newpost.html'
    model = Board
    context_object_name = 'board'


class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
