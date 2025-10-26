from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    path('', views.agendar_cita_view, name='agendar_cita'), 
    
    path('confirmada/<int:cita_id>/', views.cita_confirmada_view, name='cita_confirmada'),
    path('agendar/', views.agendar_cita_view, name='agendar_cita'),
    path('api/horas-disponibles/', views.obtener_horas_disponibles, name='obtener_horas_disponibles'),
    path('lista/', views.lista_citas_view, name='lista_citas'),

]