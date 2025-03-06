from django.urls import path
from .views import home

urlpatterns = [
    path('base/', home, name='base-home'),  
]