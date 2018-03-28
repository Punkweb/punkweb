from django.conf.urls import url

from apps.links import views

app_name = 'links'

urlpatterns = [
    url(r'^$', views.links_view, name='list'),
]
