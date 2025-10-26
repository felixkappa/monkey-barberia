from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cortes, name='lista_cortes'),
]