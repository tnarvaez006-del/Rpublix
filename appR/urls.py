from django.urls import path
from .import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('', views.login_view, name="login"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('usuarios/', views.usuarios_view, name='list'),
    path('inicio/', views.dasboard_layaut_Principal_view, name='inicio'),

    path('usuarios/editar/<int:user_id>/', views.editar_usuario, name="editar_usuario"),
    path("usuarios/agregar/", views.agregar_usuario_view, name="agregar_usuario"),
    path('usuarios/deshabilitar/<int:user_id>/', views.deshabilitar_usuario, name="deshabilitar_usuario"),
    path('usuarios/habilitar/<int:user_id>/', views.habilitar_usuario, name="habilitar_usuario"),
    path('usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name="eliminar_usuario"),


    path("clientes/", views.clientes_list, name="clientes_list"),
    path("clientes/agregar/", views.cliente_agregar, name="cliente_agregar"),
    path("clientes/editar/<int:id>/", views.cliente_editar, name="cliente_editar"),
    path("mis-tareas/", views.tareas_usuario, name="mis_tareas"),
     path(
        "tareas/completar/<int:tarea_id>/",
        views.completar_tarea,
        name="completar_tarea"
    ),

    path(
        "tareas/eliminar/<int:tarea_id>/",
        views.eliminar_tarea,
        name="eliminar_tarea"
    ),
    


    path("ordenes/", views.ordenes_list, name="ordenes_list"),
    path("ordenes/nueva/", views.crear_orden, name="orden_create"),
    path("ordenes/<int:orden_id>/", views.orden_detail, name="orden_detail"),
    path("ordenes/<int:orden_id>/editar/", views.orden_edit, name="orden_edit"),
    path("ordenes/eliminar/<int:pk>/", views.orden_delete, name="orden_delete"),

   
path("orden/revision/<int:orden_id>/", views.orden_revision, name="orden_revision"),


]
