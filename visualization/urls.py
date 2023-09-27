from django.urls import path
from . import views

app_name = 'visualization'

urlpatterns = [
    # /visualization/
    path('', views.visualize_data, name='visualize_data'),
]
