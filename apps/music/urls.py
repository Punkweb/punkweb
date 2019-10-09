from django.conf.urls import url, include

from apps.music import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^artist/(?P<slug>[\w-]+)/$', views.artist_view, name='artist'),
    url(r'^album/(?P<slug>[\w-]+)/$', views.album_view, name='album'),
    url(r'^audio/(?P<slug>[\w-]+)/$', views.audio_view, name='audio'),
]
