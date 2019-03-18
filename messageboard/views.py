from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.generic import DetailView, TemplateView, FormView

from messageboard.models import Board
from messageboard.forms import LoginForm


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
        board = get_object_or_404(Board, pk=kwargs['pk'])
        context['board'] = board
        context['title'] = board.name
        posts = [post for post in board.posts.all()]
        context['posts'] = posts
        return context


class NewPost(LoginRequiredMixin, DetailView):
    template_name = 'newpost.html'
    model = Board
    context_object_name = 'board'


class LoginSignupView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    LoginView
