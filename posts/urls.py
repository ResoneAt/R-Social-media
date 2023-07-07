from django.urls import path
from .views import CreatePostView,DetailPostView,EditPostView,DeletePostView,\
    LikePostView, DislikePostView


app_name = 'posts'
urlpatterns = [
    path('posts/create/', CreatePostView.as_view(), name='create_post'),
    path('posts/detail/<slug:slug>', DetailPostView.as_view(), name='detail_post'),
    path('posts/edit/<int:post_id>', EditPostView.as_view(), name='edit_post'),
    path('posts/delete/<int:post_id>', DeletePostView.as_view(), name='delete_post'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like_post'),
    path('posts/<int:post_id>/dislike/', DislikePostView.as_view(), name='dislike_post'),
]
