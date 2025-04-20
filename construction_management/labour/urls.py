from django.urls import path
from . import views

app_name = 'labour'

urlpatterns = [
    # Labourer URLs
    path('', views.labour_list, name='labour_list'),
    path('add/', views.labour_add, name='labour_add'),
    path('<int:pk>/edit/', views.labour_edit, name='labour_edit'),
    path('<int:pk>/delete/', views.labour_delete, name='labour_delete'),
    path('types/', views.labour_types_api, name='labour_types_api'),
    # WorkLog URLs
    path('worklog/', views.worklog_list, name='worklog_list'),
    path('worklog/add/', views.worklog_add, name='worklog_add'),
    path('worklog/<int:pk>/edit/', views.worklog_edit, name='worklog_edit'),
]
