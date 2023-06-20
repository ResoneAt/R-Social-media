from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from .forms import SignupUserForm
from .models import RelationModel
from .models import User
from django.contrib.auth import login, logout


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
    def get(self, request):
        ...

    def post(self, request):
        ...


class LogoutView(View):
    ...


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

