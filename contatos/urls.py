"""
URL configuration for contatos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.cadastrar, name='cadastrar')
Class-based views
    1. Add an import:  from other_app.views import CadastrarView
    2. Add a URL to urlpatterns:  path('', cadastrar.as_view(), name='cadastrar')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from base import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')), 
    path('cadastrar/', views.cadastrarPage, name='cadastrar'),
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve arquivos de mídia em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
