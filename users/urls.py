from django.urls import path
from users.views import sign_up,activate_user_account,assign_role,no_permission, CustomLoginView, CustomGroupListView, CustomCreateGroupView,CustomGroupDeleteView,UserProfileView,UpdateProfileView,CustomPasswordChangeView,CustomPasswordResetView, CustomPasswordResetConfirmView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('no-permission/', no_permission, name='no-permission'),
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    path('sign-out/', login_required(LogoutView.as_view()), name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', activate_user_account),
    path('admin/create-group/', CustomCreateGroupView.as_view(), name='create-group'),
    path('admin/group-list/', CustomGroupListView.as_view(), name='group-list'),
    path('admin/delete-group/<int:id>/', CustomGroupDeleteView.as_view(), name='delete-group'),
    path('admin/assign-role/<int:id>/', assign_role, name='assign-role'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='change-password'),
    path('reset-password/', CustomPasswordResetView.as_view(), name='reset-password'),
    path('reset-password/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm')
]
