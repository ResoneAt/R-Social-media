from django.urls import path
from .views import CreatePostView,DetailPostView,EditPostView,DeletePostView


app_name = 'posts'
urlpatterns = [
    path('posts/create/', CreatePostView.as_view(), name='create_post'),
    path('posts/detail/<>', DetailPostView.as_view(), name='detail_post'),
    path('posts/edit/<>', EditPostView.as_view(), name='edit_post'),
    path('posts/delete/<>', DeletePostView.as_view(), name='delete_post')
]
