from django.urls import path
from .views import CreatePostView,DetailPostView,EditPostView,DeletePostView


app_name = 'posts'
urlpatterns = [
    path('posts/create/', CreatePostView.as_view(), name='create_post'),
    path('posts/detail/<slug:slug>', DetailPostView.as_view(), name='detail_post'),
    path('posts/edit/<slug:slug>', EditPostView.as_view(), name='edit_post'),
    path('posts/delete/<slug:slug>', DeletePostView.as_view(), name='delete_post')
]
