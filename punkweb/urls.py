"""punkweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

from punkweb import settings
from punkweb import views
from admin_templates import admin_views

app_name = 'punkweb'

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^links/$', views.links_view, name='links'),
    url(r'^pgp/$', views.pgp_view, name='pgp'),
    url(
        r'^admin/templates/$',
        admin_views.templates_list,
        name='admin-template-list',
    ),
    url(
        r'^admin/templates/(?P<key>.+)/$',
        admin_views.template_view,
        name='admin-template-detail',
    ),
    url(r'^admin/', admin.site.urls),
    url(r'^board/', include('punkweb_boards.urls')),
    url(r'^board/page/', include('punkweb_boards.page_urls')),
    url(r'^board/api/', include('punkweb_boards.rest.urls')),
    url(r'^captcha/', include('captcha.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
