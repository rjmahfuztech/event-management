from django.urls import path
from users.views import sign_up, sign_in,sign_out,activate_user_account,create_group,group_list,delete_group,assign_role,no_permission

urlpatterns = [
    path('no-permission/', no_permission, name='no-permission'),
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', activate_user_account),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list/', group_list, name='group-list'),
    path('admin/delete-group/<int:id>/', delete_group, name='delete-group'),
    path('admin/assign-role/<int:id>/', assign_role, name='assign-role')
]
