from django.conf.urls import url
from . import views

app_name='user_app'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^register$', views.register, name = 'register'),
    url(r'^logout$', views.logout, name = 'logout'),
    url(r'^user(?P<id>\d+)$', views.user, name = 'user'),
    url(r'^settings/(?P<user_id>\d+)/', views.settings, name='settings'),
    url(r'^update_information(?P<user_id>\d+)$', views.update_information, name = 'update_information'),
    url(r'^delete(?P<user_id>\d+)$', views.delete, name = 'delete'),
]
