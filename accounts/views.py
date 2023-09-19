from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import View
from .forms import (
    SignupUserForm,
    LoginUserForm,
    EditProfileForm,
    ReportUserForm,
    MessageForm,
)
from .models import User, MessageModel
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)


class SignupView(View):
    form_class = SignupUserForm
    template_name = "accounts/signup_form.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"signup_form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                email=cd["email"], username=cd["username"], password=cd["password1"]
            )
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("home:home")
        return render(request, self.template_name, {"signup_form": form})


class LoginView(View):
    form_class = LoginUserForm
    template_name = "accounts/login_form.html"

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"login_form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                login(request, user)
                messages.success(request, "You logged in successfully", "success")
                if self.next:
                    return redirect(self.next)
                return redirect("home:home")
            messages.error(request, "username or password is wrong!", "danger")
        return render(request, self.template_name, {"login_form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.warning(request, "you are logout ...", "warning")
            return redirect("accounts:login")
        messages.error(request, "you can not do this action", "danger")
        return redirect("home:home")


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id, is_active=True)
        is_following = User.is_following(request.user, user_id)
        is_follow_requesting = User.is_follow_requesting(request.user, user_id)
        context = {
            "is_follow_requesting": is_follow_requesting,
            "is_following": is_following,
            "user": user,
        }
        return render(request, "accounts/profile.html", context)


class EditProfileView(LoginRequiredMixin, View):
    form_class = EditProfileForm
    template_name = "accounts/edit_profile.html"

    def get(self, request, user_id):
        if request.user.id == user_id:
            form = self.form_class(instance=request.user)
            return render(request, self.template_name, {"form": form})
        messages.error(request, "You can not do this action!", "danger")
        return redirect("home:home")

    def post(self, request, user_id):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:user_profile", request.user.id)
        return render(request, self.template_name, {"form": form})


class DeleteAccountView(LoginRequiredMixin, View):
    template_name = "accounts/confirm_delete_account.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.id == kwargs["user_id"]:
            messages.error(request, "You can not do this action!", "danger")
            return redirect("accounts:user_profile", kwargs["user_id"])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        return render(request, self.template_name)

    def post(self, request, user_id):
        request.user.delete()
        return redirect("accounts:login")


class FollowView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if User.is_privet(kwargs["user_id"]):
            messages.error(
                request,
                "you can not follow this user. this account is privet!",
                "danger",
            )
            return redirect("accounts:user_profile", kwargs["user_id"])
        if User.is_following(request.user, kwargs["user_id"]):
            messages.error(request, "you can not follow this user again!", "danger")
            return redirect("accounts:user_profile", kwargs["user_id"])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        User.follow(request.user, user_id)
        messages.success(request, "your following success", "success")
        return redirect("accounts:user_profile", user_id)


class UnFollowView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not User.is_following(request.user, kwargs["user_id"]):
            messages.error(request, "you can not unfollow this user", "warning")
            return redirect("accounts:user_profile", kwargs["user_id"])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        User.unfollow(request.user, user_id)
        messages.success(request, "your Unfollowing success", "success")
        return redirect("accounts:user_profile", user_id)


class FollowerListView(LoginRequiredMixin, View):
    template_name = "accounts/follower_list.html"

    def get(self, request, user_id):
        if User.is_following(request.user, user_id) or request.user.id == user_id:
            follower = User.get_follower_list(user_id)
            return render(request, self.template_name, {"follower": follower})
        return redirect("accounts:user_profile", user_id)


class FollowingListView(LoginRequiredMixin, View):
    template_name = "accounts/following_list.html"

    def get(self, request, user_id):
        if User.is_following(request.user, user_id) or request.user.id == user_id:
            following = User.get_following_list(user_id)
            return render(request, self.template_name, {"following": following})
        return redirect("accounts:user_profile", user_id)


class SentFollowRequest(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not User.is_privet(kwargs["user_id"]):
            messages.error(request, "you can not sent request to this user", "danger")
            return redirect("accounts:user_profile", kwargs["user_id"])
        if User.is_follow_requesting(request.user, kwargs["user_id"]):
            messages.error(request, "You have already sent a request!", "danger")
            return redirect("accounts:user_profile", kwargs["user_id"])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        User.follow_request(request.user, user_id)
        messages.success(request, "your request sent success", "success")
        return redirect("accounts:user_profile", user_id)


class FollowRequestList(LoginRequiredMixin, View):
    def get(self, request):
        requests = User.get_requests_list(request.user)
        return render(request, "accounts/request_list.html", {"requests": requests})


class AcceptFollowRequest(LoginRequiredMixin, View):
    def get(self, request, user_id):
        User.accept_follow_request(request.user, user_id)
        messages.success(request, "your Accept request success", "success")
        return redirect("accounts:follow_request_list")


class RejectFollowRequest(LoginRequiredMixin, View):
    def get(self, request, user_id):
        User.reject_follow_request(request.user, user_id)
        messages.success(request, "you are Reject request", "success")
        return redirect("accounts:follow_request_list")


class ReportUserView(LoginRequiredMixin, View):
    class_form = ReportUserForm
    template_name = "accounts/report.html"

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        form = self.class_form()
        context = {"reported_user": user, "form": form}
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        form = self.class_form(request.POST)
        user = get_object_or_404(User, pk=user_id)
        context = {"reported_user": user, "form": form}
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.user_reported = user
            report.save()
            messages.success(request, "Your report has been sent", "success")
            return redirect("accounts:user_profile", user_id)
        else:
            return render(request, self.template_name, context)


class SentMessagesView(LoginRequiredMixin, View):
    template_name = "accounts/pv_messages.html"

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        form = MessageForm()
        messages_list = MessageModel.objects.filter(
            from_user=request.user, to_user=user
        ) | MessageModel.objects.filter(from_user=user, to_user=request.user)
        messages_list = messages_list.order_by("created_at")
        context = {
            "form": form,
            "user": user,
            "messages_list": messages_list,
        }
        MessageModel.seen_message(user_id, request.user.id)
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.from_user = request.user
            message.to_user = user
            message.save()
        return redirect("accounts:message", user.id)


class MessagesListView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.filter(
            Q(sender__to_user=request.user) | Q(receiver__from_user=request.user)
        ).distinct()
        context = {"users": users}
        return render(request, "accounts/chat_list.html", context)


class UserPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset_form.html"
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
