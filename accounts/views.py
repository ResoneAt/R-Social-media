from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from .forms import SignupUserForm, LoginUserForm, EditProfileForm
from .authenticate import UsernameBackend
from .models import RelationModel
from .models import User
from django.contrib.auth import login, logout, authenticate


class SignupView(View):
    form_class = SignupUserForm
    template_name = 'accounts/signup_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'signup_form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(email=cd['email'], username=cd['username'], password=cd['password1'])
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home:home')
        return render(request, self.template_name, {'signup_form': form})


class LoginView(View):
    form_class = LoginUserForm
    template_name = 'accounts/login_form.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'login_form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],password=cd['password'])
            if user is not None:
                login(request, user)
                # messages.success(request, 'You logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            # messages.error(request, 'username or password is wrong!', 'danger')
        return render(request, self.template_name, {'login_form': form})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            # messages.warning(request, 'you are logout ...', 'warning')
            return redirect('accounts:login')
        # messages.error(request, 'you can not do this action', 'danger')
        return redirect('home:home')


class ProfileView(View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        return render(request, 'accounts/profile.html', {'user':user})


class EditProfileView(View):
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'

    def get(self, request, user_id):
        if request.user.id == user_id:
            form = self.form_class(instance=request.user)
            return render(request, self.template_name, {'form': form})
        return redirect('home:home')

    def post(self, request, user_id):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:user_profile', request.user.id)
        return render(request, self.template_name, {'form': form})


class DeleteAccountView(View):
    template_name = 'accounts/confirm_delete_account.html'

    def get(self, request, user_id):
        if request.user.id == user_id:
            return render(request, self.template_name)
        return redirect('home:home')

    def post(self, request, user_id):
        if request.user.id == user_id:
            user = request.user
            user.is_active = False
            user.save()
            return redirect('accounts:login')
        return render(request, self.template_name)


class FollowView(View):
    def get(self, request, user_id):
        if request.user.account_type == 'public':
            if not User.is_following(request.user, user_id):
                User.follow(request.user, user_id)
                messages.success(request, 'your following success', 'success')
            else:
                messages.error(request, 'you can not follow this user again!', 'danger')
            return redirect('accounts:user_profile', user_id)
        messages.error(request, 'you can not follow this user. this account is privet!', 'danger')
        return redirect('accounts:user_profile', user_id)


class UnFollowView(View):
    def get(self, request, user_id):
        if User.is_following(request.user, user_id):
            User.unfollow(request.user, user_id)
            messages.success(request, 'your Unfollowing success', 'success')
        else:
            messages.error(request, 'you can not unfollow this user', 'warning')
        return redirect('accounts:user_profile', user_id)


class FollowerListView(View):
    template_name = 'accounts/follower_list.html'

    def get(self, request, user_id):
        if User.is_following(request.user, user_id):
            follower = User.get_follower_list(user_id)
            return render(request, self.template_name, {'follower': follower})
        return redirect('accounts:user_profile', user_id)


class FollowingListView(View):
    template_name = 'accounts/following_list.html'

    def get(self, request, user_id):
        if User.is_following(request.user, user_id):
            following = User.get_following_list(user_id)
            return render(request, self.template_name, {'following': following})
        return redirect('accounts:user_profile', user_id)


class SentFollowRequest(View):
    def get(self, request, user_id):
        if User.is_privet(user_id):
            User.follow_request(request.user, user_id)
        return redirect('accounts:user_profile', user_id)


class FollowRequestList(View):
    ...


class AcceptFollowRequest(View):
    ...


class RejectFollowRequest(View):
    ...


class ReportUserView(View):
    ...


class SentMessagesView(View):
    ...


class MessagesListView(View):
    ...


class MessagePrivetPageView(View):
    ...

