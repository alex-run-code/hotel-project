from . import views
from django.urls import path

urlpatterns = [
    path('units', views.UnitList.as_view(), name='units')
]