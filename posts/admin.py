from django.contrib import admin
from .models import PostModel, MoviePostModel,ImagePostModel,ReportPostModel,CommentModel,LikeModel
# Register your models here.


class PostImageInline(admin.TabularInline):
    model = ImagePostModel


class PostMovieInline(admin.TabularInline):
    model = MoviePostModel


class CommentInline(admin.TabularInline):
    model = CommentModel


class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline, PostMovieInline, CommentInline]
    prepopulated_fields = {'slug': ('body',)}


admin.site.register(PostModel, PostAdmin)
admin.site.register(ReportPostModel)
admin.site.register(CommentModel)
admin.site.register(LikeModel)
