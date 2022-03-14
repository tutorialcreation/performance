"""setup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # change url in production --> performancesuits.com/_&_wysiwyg-suits_empty-link_url
    path('', views.index_view, name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('task-master/', include('taskmanager.urls')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('select2/', include('django_select2.urls')),
    path('bs_index/',views.bootstrap_index),
    path('crm/',include('crm.urls',namespace='crm')),

    # path('accounts/', include('allauth.urls')),
]

urlpatterns += [
    path('pams_system/', include('pams_system.urls')),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
admin.site.site_header = 'performance ADMINISTRATION'

admin.autodiscover()
admin.site.enable_nav_sidebar = False