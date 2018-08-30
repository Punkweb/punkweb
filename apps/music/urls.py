from django.conf.urls import url, include

from apps.music import views

app_name = 'stream'

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^audio/(?P<slug>[\w-]+)/$', views.audio_view, name='audio'),
    url(r'^audio/compilation/(?P<slug>[\w-]+)/$',
        views.audio_compilation_view, name='audio_compilation'),
]
