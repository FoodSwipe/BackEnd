from django.urls import path

from accounts.views.accounts import (AddUser, ListUser, RegisterFollower,
                                     RegisterUser, RegistrationSummaryListView,
                                     ToggleStaffUserStatus,
                                     ToggleSuperUserStatus,
                                     UpdateUserWithProfile, UserDetail)
from accounts.views.login import LoginView, LogoutView
from accounts.views.password import (ResetPasswordConfirm,
                                     ResetPasswordRequestCode, UpdatePassword)
from accounts.views.profile import (ListProfile, ListProfiles, ProfileDetail,
                                    UserProfileContactListView)

app_name = "accounts"

urlpatterns = [
    path("user", ListUser.as_view(), name="users-list"),
    path("user/<int:pk>", UserDetail.as_view(), name="user-detail"),
    path(
        "user/<int:pk>/toggle-superuser-status",
        ToggleSuperUserStatus.as_view(),
        name="toggle-superuser-status",
    ),
    path(
        "user/<int:pk>/toggle-staff-status",
        ToggleStaffUserStatus.as_view(),
        name="toggle-staff-status",
    ),
    path("profiles", ListProfiles.as_view(), name="list-profiles"),
    path("user/<int:pk>/profile", ListProfile.as_view(), name="profile-list"),
    path("profile/<int:pk>", ProfileDetail.as_view(), name="profile-detail"),
    path("login", LoginView.as_view(), name="swipe_login"),
    path("logout", LogoutView.as_view(), name="swipe_logout"),
    path("user/update-password", UpdatePassword.as_view(), name="update-password"),
    path(
        "user/reset-password",
        ResetPasswordRequestCode.as_view(),
        name="reset-password-request",
    ),
    path(
        "user/reset-password/<str:code>/",
        ResetPasswordConfirm.as_view(),
        name="reset-password-confirm",
    ),
    path(
        "registration-summary",
        RegistrationSummaryListView.as_view(),
        name="registration-summary",
    ),
    path(
        "list-user-contacts",
        UserProfileContactListView.as_view(),
        name="profile-contact-filter",
    ),
    path("register", RegisterUser.as_view(), name="register-user"),
    path("register-follower", RegisterFollower.as_view()),
    path("add-user", AddUser.as_view(), name="add-user"),
    path(
        "user-update/<int:pk>",
        UpdateUserWithProfile.as_view(),
        name="update-user-profile",
    ),
]
