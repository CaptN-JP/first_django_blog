from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)

""" urlpatterns is a predefined variable, therefore changing its name to url_pattern yeilded an error
Also use comma " , " to separate different path's
"""

urlpatterns = [
    # path("", views.home, name ='blog-home'),
    path("", PostListView.as_view(), name='blog-home'),
    path("user/<str:username>", UserPostListView.as_view(), name='user-posts'),
    path("post/<int:pk>", PostDetailView.as_view(), name='post-detail'),
    path("post/new", PostCreateView.as_view(), name='post-create'),
    path("post/<int:pk>/update", PostUpdateView.as_view(), name='post-update'),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name='post-delete'),
    path("about/", views.about, name='blog-about')
]