from django.shortcuts import render
from django.views.generic import View


class SignupView(View):
    def get(self, request):
        ...

    def post(self, request):
        ...


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

