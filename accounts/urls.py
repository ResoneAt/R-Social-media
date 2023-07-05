from django.urls import path
from .views import SignupView, LoginView, LogoutView,\
    ProfileView, EditProfileView, DeleteAccountView,\
    FollowView, UnFollowView, FollowerListView, FollowingListView,\
    SentFollowRequest, FollowRequestList, AcceptFollowRequest, RejectFollowRequest,\
    ReportUserView, SentMessagesView, MessagesListView


app_name = 'accounts'
urlpatterns = [
    path('accounts/signup-user/', SignupView.as_view(), name='signup'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/profile/<int:user_id>/', ProfileView.as_view(), name='user_profile'),
    path('accounts/profile/edit/<int:user_id>/', EditProfileView.as_view(), name='edit_profile'),
    path('accounts/profile/<int:user_id>/follower/', FollowerListView.as_view(), name='follower_list'),
    path('accounts/profile/<int:user_id>/following/', FollowingListView.as_view(), name='following_list'),
    path('accounts/profile/delete/<int:user_id>/', DeleteAccountView.as_view(), name='delete_account'),
    path('accounts/profile/report/<int:user_id>/', ReportUserView.as_view(), name='report_user'),
    path('accounts/profile/chat-list/<int:user_id>/', SentMessagesView.as_view(), name='message'),
    path('accounts/profile/chat-list/', MessagesListView.as_view(), name='chat_list'),
    path('accounts/follow/<int:user_id>/', FollowView.as_view(), name='follow'),
    path('accounts/unfollow/<int:user_id>/', UnFollowView.as_view(), name='unfollow'),
    path('accounts/follow_request/<int:user_id>/', SentFollowRequest.as_view(), name='follow_request'),
    path('accounts/follow_request_list/', FollowRequestList.as_view(), name='follow_request_list'),
    path('accounts/follow_request_list/accept/<int:user_id>/', AcceptFollowRequest.as_view(), name='accept_request'),
    path('accounts/follow_request_list/reject/<int:user_id>/', RejectFollowRequest.as_view(), name='reject_request'),
]
