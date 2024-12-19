from django.urls import path
from .views import add_robot
from .views import download_production_list


urlpatterns = [
    path('api/robots/', add_robot, name='add_robot'),
    path('download/production-list/', download_production_list, name='download_production_list')
]
