from django.urls import path
from .import views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('usuarios/', views.usuarios_view, name='list'),
    path('inicio/', views.dasboard_layaut_Principal_view, name='inicio'),

    path('usuarios/editar/<int:user_id>/', views.editar_usuario, name="editar_usuario"),
    path("usuarios/agregar/", views.agregar_usuario_view, name="agregar_usuario"),
    path('usuarios/deshabilitar/<int:user_id>/', views.deshabilitar_usuario, name="deshabilitar_usuario"),
    path('usuarios/habilitar/<int:user_id>/', views.habilitar_usuario, name="habilitar_usuario"),
    path('usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name="eliminar_usuario"),
]
