from django.contrib.auth.views import LogoutView
from django.urls import path

from messageboard import views

urlpatterns = [
    path('', views.TemplateView.as_view(template_name="home.html", extra_context={"title": "Home"}), name="home"),
    path('board/<str:pk>', views.BoardView.as_view(), name='boardview'),
    path('board/<str:pk>/newpost', views.NewPost.as_view(), name='newpost'),
    path('login', views.LoginSignupView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='/'), name='logout'),
    path('newboard', views.NewBoardView.as_view(), name="newboard"),
    path('posts', views.UserPostsView.as_view(), name="posts"),
    path('posts/<str:pk>/delete', views.DeletePostView.as_view(), name="deletepost")
]
