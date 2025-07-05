from django.urls import path
from .views import (
  CompleteRegistrationView, 
  MeView, 
  CreateUserView, 
  ChangePasswordView, 
  UserListView,
  LogoutView,
)

urlpatterns = [
  path('logout/', LogoutView.as_view(), name='logout'),
  path('me/', MeView.as_view(), name='me'),
  path('', UserListView.as_view(), name='user-list'),
  path('create/', CreateUserView.as_view(), name='user-create'),
  path('change-password/', ChangePasswordView.as_view(), name='change-password'),
  path('complete-registration/', CompleteRegistrationView.as_view(), name='complete-registration'),
]