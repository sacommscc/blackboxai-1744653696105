from django.urls import path
from . import views

app_name = 'contractors'

urlpatterns = [
    path('', views.contractor_list_create, name='contractor_list_create'),
    path('<int:pk>/', views.contractor_detail, name='contractor_detail'),
    path('<int:contractor_id>/payments/', views.contractor_payments, name='contractor_payments'),
]
