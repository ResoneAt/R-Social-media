from django.urls import path
from .views import SignupView, LoginView, LogoutView, ProfileView


app_name = 'accounts'
urlpatterns = [
    path('accounts/signup/', SignupView.as_view(), name='signup'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/profile/<int:user_id>', ProfileView.as_view(), name='user_profile')
]
