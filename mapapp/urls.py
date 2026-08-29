from django.urls import path
from . import views

app_name = 'mapapp'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('mapa/', views.mapa, name='mapa'),
    path('acerca/', views.acerca, name='acerca'),
    path('api/puntos/', views.api_puntos, name='api_puntos'),
    path('api/puntos/<int:pk>/', views.api_punto_detalle, name='api_punto_detalle'),
    path('api/playas/<str:pk>/', views.api_playa_detalle, name='api_playa_detalle'),
    path('api/fotos/<str:filename>', views.serve_foto, name='serve_foto'),
    path('api/tramos/', views.api_tramos, name='api_tramos'),
    path('api/tramos/<int:pk>/', views.api_tramo_detalle, name='api_tramo_detalle'),
    path('api/celdas/', views.api_celdas, name='api_celdas'),
    path('api/celdas/<int:pk>/', views.api_celda_detalle, name='api_celda_detalle'),
    path('api/subceldas/', views.api_subceldas, name='api_subceldas'),
    path('api/subceldas/<int:pk>/', views.api_subcelda_detalle, name='api_subcelda_detalle'),
    path('api/modelacion/', views.api_modelacion, name='api_modelacion'),
    path('api/pastos/', views.api_pastos, name='api_pastos'),
    path('api/dunas/', views.api_dunas, name='api_dunas'),
    path('api/manglares/', views.api_manglares, name='api_manglares'),
    path('api/crestas/', views.api_crestas, name='api_crestas'),
    path('api/antropizacion/', views.api_antropizacion, name='api_antropizacion'),
]
