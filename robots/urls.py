from django.urls import path
from .views import add_robot


urlpatterns = [
    path('api/robots/', add_robot, name='add_robot'),
]