from django.db import models
from accounts.models import User
# Create your models here.


class PostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField()
    location = models.CharField(max_length=730,blank=True, null=True)
    created_time = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.slug


class ImagePostModel(models.Model):
    image = models.ImageField(upload_to='posts')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='image')
    alt = models.CharField(max_length=73)

    def __str__(self):
        return self.alt


class MoviePostModel(models.Model):
    movie = models.FileField(upload_to='posts_movie')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)


class ReportPostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reporter')
    post = models.ForeignKey(PostModel, on_delete=models.PROTECT, related_name='reported_post')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post} - {self.body[:20]}'


class LikeModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='liked_post')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post}-{self.user.username}'


class CommentModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    body = models.TextField()
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comment')
    created_at = models.DateTimeField(auto_now_add=True)
    replay_to = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    is_replay = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author.username} - {self.body[:20]} - {self.post}'
