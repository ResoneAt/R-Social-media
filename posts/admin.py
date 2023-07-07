from django.contrib import admin
from .models import PostModel, MoviePostModel,ReportPostModel,CommentModel,LikeModel,RecyclePost
# Register your models here.


class PostMovieInline(admin.TabularInline):
    model = MoviePostModel


class CommentInline(admin.TabularInline):
    model = CommentModel


class PostAdmin(admin.ModelAdmin):
    inlines = [PostMovieInline, CommentInline]
    prepopulated_fields = {'slug': ('body',)}


@admin.register(RecyclePost)
class RecycleUserAdmin(admin.ModelAdmin):

    actions = ['recover']

    def get_queryset(self, request):
        return RecyclePost.deleted.filter(is_active=False, is_deleted=True)

    @admin.action(description="Recover deleted item")
    def recover(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None, is_active=True)


admin.site.register(PostModel, PostAdmin)
admin.site.register(ReportPostModel)
admin.site.register(CommentModel)
admin.site.register(LikeModel)
