from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),  # first page
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('apply/', views.apply_leave, name='apply_leave'),
    path('edit/<int:id>/', views.edit_leave, name='edit_leave'),
    path('my-leaves/', views.my_leaves, name='my_leaves'),
    path('admin-dashboard/', views.admin_home, name='admin_dashboard'),
    path('leave-requests/', views.admin_dashboard, name='leave_requests'),
    path('approve/<int:id>/', views.approve_leave),
    path('reject/<int:id>/', views.reject_leave),
    path('delete/<int:id>/', views.delete_leave),
    path('users/', views.manage_users, name='manage_users'),
    path('edit-user/<int:id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),
    path('reset-password/<int:id>/', views.reset_password, name='reset_password'),
]