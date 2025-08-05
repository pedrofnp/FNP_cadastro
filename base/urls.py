from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [

    # Redireciona a raiz para a página de cadastro
    path('', RedirectView.as_view(url='/cadastrar/', permanent=False)),

    # Páginas principais
    path('cadastrar/', views.cadastrarPage, name='cadastrar'),
    path('procurar/', views.procurarPage, name='procurar'),
    path('consulta/<int:contato_id>/', views.consulta, name='consulta'),
    path('mapa_municipio/', views.mapa_municipioPage, name='mapa_municipio'),  # unificada

    # Autenticação
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    # API de informações de um município
    path('api/municipio/<str:nome_municipio>/', views.municipio_info_api, name='municipio_info_api'),

    # API que retorna todos os municípios
    path('get-municipios/', views.get_municipios, name='get_municipios'),

    # API de edição via AJAX
    path('api/editar_municipio/', views.editar_municipio_ajax, name='editar_municipio_ajax'),

    # Exportações CSV
    path('exportar-estados-csv/', views.exportar_estados_csv, name='exportar_estados_csv'),
    path('exportar-cargos-csv/', views.exportar_cargos_csv, name='exportar_cargos_csv'),
    path('exportar-partidos-csv/', views.exportar_partidos_csv, name='exportar_partidos_csv'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
