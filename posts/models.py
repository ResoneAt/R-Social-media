from django.db import models
from django.urls import reverse
from accounts.models import User
from core.models import BaseModel
# Create your models here.


class PostModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField()
    location = models.CharField(max_length=730,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.slug

    def comment_count(self):
        return self.comment.count()

    def like_count(self):
        return self.liked_post.count()

    def get_comments_list(self):
        return CommentModel.objects.filter(post=self)

    def get_liker_list(self):
        return User.objects.filter(liker__post=self)

    def post_images(self):
        return ImagePostModel.objects.filter(post=self)

    def post_movies(self):
        return MoviePostModel.objects.filter(post=self)

    def get_report_list(self):
        return ReportPostModel.objects.filter(post=self)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug
        }
        return reverse('post_detail', kwargs=kwargs)


class ImagePostModel(models.Model):
    image = models.ImageField(upload_to='posts')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='image')
    alt = models.CharField(max_length=73)

    def __str__(self):
        return self.alt


class MoviePostModel(models.Model):
    movie = models.FileField(upload_to='posts_movie')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)


class ReportPostModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reporter')
    post = models.ForeignKey(PostModel, on_delete=models.PROTECT, related_name='reported_post')
    body = models.TextField()

    def __str__(self):
        return f'{self.post} - {self.body[:20]}'


class LikeModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='liked_post')

    def __str__(self):
        return f'{self.post}-{self.user.username}'


class CommentModel(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    body = models.TextField()
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comment')
    replay_to = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    is_replay = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author.username} - {self.body[:20]} - {self.post}'
