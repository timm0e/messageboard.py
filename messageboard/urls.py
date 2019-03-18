from django.contrib.auth.views import LogoutView
from django.urls import path

from messageboard import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('board/<str:pk>', views.BoardView.as_view(), name='boardview'),
    path('board/<str:pk>/newpost', views.NewPost.as_view(), name='newpost'),
    path('login', views.LoginSignupView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='/'), name='logout')
]
