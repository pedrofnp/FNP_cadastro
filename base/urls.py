from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.homePage, name='home'),
    path('home/', views.homePage, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('get-municipios/<int:estado_id>/', views.get_municipios, name='get_municipios'),
    path('dash/', views.dashPage, name='dash'),
    path('editar-contato/<int:contato_id>/', views.editar_contato, name='editar_contato'),
    path('exportar-estados-csv/', views.exportar_estados_csv, name='exportar_estados_csv'),
    path('exportar-cargos-csv/', views.exportar_cargos_csv, name='exportar_cargos_csv'),
    path('exportar-municipios-csv/', views.exportar_municipios_csv, name='exportar_municipios_csv'),
    path('exportar-partidos-csv/', views.exportar_partidos_csv, name='exportar_partidos_csv'),
    path('mapa/', views.mapa_view, name='mapa'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)