from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('predict/', views.predict, name='predict'),
    path('history/', views.prediction_history, name='prediction_history'),
    path('contact/', views.contact, name='contact'),
    # Admin
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', views.manage_users, name='manage_users'),
    path('admin-panel/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin-panel/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin-panel/users/toggle/<int:user_id>/', views.toggle_user, name='toggle_user'),
    path('admin-panel/predictions/', views.admin_predictions, name='admin_predictions'),
]
