from django.urls import path
from . import views

urlpatterns = [
    # URLs para Home-index-inicio
    path('', views.inicio, name='inicio'),  # Esta ruta carga la vista 'inicio'
    # URLs para Campistas
    path('listadoCampistas/', views.listadoCampistas, name='listado_campistas'),

    path('nuevaCampista/', views.nuevaCampista, name='nuevaCampista'),
    path('guardarCampista/', views.guardarCampista, name='guardarCampista'),
    path('editarCampista/<int:id>/', views.editarCampista, name='editarCampista'),
    path('procesoActualizarCampista/', views.procesoActualizarCampista, name='procesoActualizarCampista'),
    path('eliminarCampista/<int:id>/', views.eliminarCampista, name='eliminarCampista'),

    # URLs para Reservas
    path('listadoReservas/', views.listadoReservas, name='listado_reservas'),
    path('nuevaReserva/', views.nuevaReserva, name='nuevaReserva'),
    path('guardarReserva/', views.guardarReserva, name='guardarReserva'),
    path('editarReserva/<int:id>/', views.editarReserva, name='editarReserva'),
    path('procesoActualizarReserva/', views.procesoActualizarReserva, name='procesoActualizarReserva'),
    path('eliminarReserva/<int:id>/', views.eliminarReserva, name='eliminarReserva'),
]

