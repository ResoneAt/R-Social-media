from django.urls import path
from .views import SignupView, LoginView, LogoutView


app_name = 'accounts'
urlpatterns = [
    path('accounts/signup/', SignupView.as_view(), name='signup'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout')
]
