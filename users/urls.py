from django.urls import path
from users.views import sign_up,activate_user_account,assign_role,no_permission, CustomLoginView, CustomGroupListView, CustomCreateGroupView,CustomGroupDeleteView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('no-permission/', no_permission, name='no-permission'),
    path('sign-up/', sign_up, name='sign-up'),
    # path('sign-in/', sign_in, name='sign-in'),
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    # path('sign-out/', sign_out, name='sign-out'),
    path('sign-out/', login_required(LogoutView.as_view()), name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', activate_user_account),
    # path('admin/create-group/', create_group, name='create-group'),
    path('admin/create-group/', CustomCreateGroupView.as_view(), name='create-group'),
    # path('admin/group-list/', group_list, name='group-list'),
    path('admin/group-list/', CustomGroupListView.as_view(), name='group-list'),
    # path('admin/delete-group/<int:id>/', delete_group, name='delete-group'),
    path('admin/delete-group/<int:id>/', CustomGroupDeleteView.as_view(), name='delete-group'),
    path('admin/assign-role/<int:id>/', assign_role, name='assign-role')
]
