from django.urls import path

from accounts.views.accounts import ListUser, UserDetail
from accounts.views.login import LoginView, LogoutView
from accounts.views.password import UpdatePassword, ResetPasswordRequestCode, ResetPasswordConfirm
from accounts.views.profile import ListProfile, ProfileDetail

app_name = "accounts"

urlpatterns = [
    path("user", ListUser.as_view(), name="users-list"),
    path("user/<int:pk>", UserDetail.as_view(), name="user-detail"),
    path("user/<int:pk>/profile", ListProfile.as_view(), name="profile-list"),
    path("profile/<int:pk>", ProfileDetail.as_view(), name="profile-detail"),
    path("login", LoginView.as_view(), name="swipe_login"),
    path("logout", LogoutView.as_view(), name="swipe_logout"),
    path("user/update-password", UpdatePassword.as_view(), name="update-password"),
    path("user/reset-password", ResetPasswordRequestCode.as_view(), name="reset-password-request"),
    path("user/reset-password/<str:code>/", ResetPasswordConfirm.as_view(), name="reset-password-confirm"),
]
