from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from .forms import SignupUserForm, LoginUserForm
from .models import RelationModel
from .models import User
from django.contrib.auth import login, logout, authenticate


class SignupView(View):
    form_class = SignupUserForm
    template_name = 'accounts/signup_form.html'

    def get(self, request):
        form = self.form_class()
        context = {'signup_form': form}
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
            login(request, user, backend='django.contrib.auth.backends.ModelBackend',)
            messages.success(request, 'your user created is successfully!', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'signup_form': form})


class LoginView(View):
    form_class = LoginUserForm
    template_name = 'accounts/login_form.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'login_form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'username or password is wrong!', 'danger')
        return render(request, self.template_name, {'login_form': form})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            # messages.warning(request, 'you are logout ...', 'warning')
            return redirect('accounts:login')
        messages.error(request, 'you can not do this action', 'danger')
        return redirect('home:home')


class ProfileView(View):
    ...


class EditProfile(View):
    ...


class DeleteAccountView(View):
    ...


class FollowView(View):
    ...


class FollowerListView(View):
    ...


class FollowingListView(View):
    ...


class UnFollowView(View):
    ...


class SentFollowRequest(View):
    ...


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

