from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('vendors/', views.vendors_list, name='vendors'),
    path('vendors/add/', views.vendors_list, name='vendor_add'),
    path('vendors/<int:id>/edit/', views.vendors_list, name='vendor_edit'),
    path('vendors/<int:id>/delete/', views.vendors_list, name='vendor_delete'),
    path('labour/', views.labour_list, name='labour'),
    path('transactions/', views.transactions_list, name='transactions'),
    path('reports/', views.reports_list, name='reports'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
