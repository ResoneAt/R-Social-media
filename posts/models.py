from django.db import models
from django.urls import reverse
from accounts.models import User
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .manager import MyPostModelManager
from django.db.models.manager import Manager
from ckeditor.fields import RichTextField


class PostModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    # body = models.TextField(help_text='Please write caption')
    body = RichTextField()

    image = models.ImageField(upload_to='posts',blank=True, null=True, help_text='Please upload your image')
    location = models.CharField(max_length=730, blank=True, null=True,
                                help_text='You can write the location of this post')
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(default='0-0')

    deleted_at = models.DateField(blank=True, null=True, editable=False)
    is_deleted = models.BooleanField(blank=True, null=True, default=False)

    objects = MyPostModelManager()

    class Meta:
        verbose_name, verbose_name_plural = _("Post"), _("Posts")

    def __str__(self):
        return self.user.email

    def comment_count(self):
        return self.comment.count()

    def like_count(self):
        return self.liked_post.count()

    def get_comments_list(self):
        return CommentModel.objects.filter(post=self)

    def get_liker_list(self):
        return User.objects.filter(liker__post=self)

    # def post_images(self):
    #     return ImagePostModel.objects.filter(post=self)

    def post_movies(self):
        return MoviePostModel.objects.filter(post=self)

    def get_report_list(self):
        return ReportPostModel.objects.filter(post=self)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def get_absolute_url(self):
        kwargs = {'slug': self.slug}
        return reverse('posts:detail_post', kwargs=kwargs)


class RecyclePost(PostModel):
    deleted = Manager()

    class Meta:
        proxy = True


class MoviePostModel(BaseModel):
    movie = models.FileField(upload_to='posts_movie', help_text='Please upload your movie file.')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name, verbose_name_plural = _("Movie"), _("Movies")


class ReportPostModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reporter_user')
    post = models.ForeignKey(PostModel, on_delete=models.PROTECT, related_name='reported_post')
    body = models.TextField(verbose_name=_('Report text'),
                            help_text='Please write the reason for reporting this post')

    class Meta:
        verbose_name, verbose_name_plural = _("Post Report"), _("Post Reports")

    def __str__(self):
        return f'{self.user.username} - {self.post.body}'


class LikeModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='liked_post')

    class Meta:
        unique_together = ('user', 'post')
        verbose_name, verbose_name_plural = _("Like"), _("Likes")

    def __str__(self):
        return f'{self.user.username} - {self.post.body}'


class CommentModel(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    body = models.TextField(verbose_name=_('comment text'),
                            help_text='Please write the comment')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comment')
    replay_to = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    is_replay = models.BooleanField(default=False)

    class Meta:
        verbose_name, verbose_name_plural = _("Comment"), _("Comments")

    def __str__(self):
        return f'{self.user.username} - {self.body} - {self.post.body}'
