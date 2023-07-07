from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,NotificationModel,ReportUserModel,\
    FollowRequestModel,MessageModel,RelationModel,RecycleUser
from .forms import UserCreationForm, UserChangeForm


# class UserImageInline(admin.TabularInline):
#     model = ImageUserModel


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "date_of_birth", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["username", "email", "password"]}),
        ("Personal info", {"fields": ["first_name","last_name","image", "bio", "gender", "phone_number" ,
                                      'account_type', "date_of_birth"]}),
        ("Permissions", {"fields": ["is_admin", "is_active", "is_deleted"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []
    # inlines = [UserImageInline]


@admin.register(RecycleUser)
class RecycleUserAdmin(admin.ModelAdmin):

    actions = ['recover']

    def get_queryset(self, request):
        return RecycleUser.deleted.filter(is_active=False, is_deleted=True)

    @admin.action(description="Recover deleted item")
    def recover(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None, is_active=True)


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
admin.site.register(MessageModel)
admin.site.register(ReportUserModel)
admin.site.register(NotificationModel)
admin.site.register(FollowRequestModel)
admin.site.register(RelationModel)
