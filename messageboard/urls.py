from django.urls import path
from django.views.generic import TemplateView

from messageboard import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('board/<str:pk>', views.BoardView.as_view(), name='boardview'),
    path('board/<str:pk>/newpost', views.NewPost.as_view(), name='newpost'),
    path('login', views.Login.as_view(), name='login')
]
