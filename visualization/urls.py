from django.urls import path
from . import views

app_name = 'visualization'

urlpatterns = [
    # /visualization/
    path('', views.visualize_data, name='visualize_data'),
    path('visualize_data_by_date/', views.visualize_data_by_date, name='visualize_data_by_date'),
]
