from django.conf.urls import url

from . import views

app_name = "message_app"

urlpatterns = [
    url(r"^$", views.index, name = "index"),
    url(r"^newmessage$", views.newmessage, name = "newmessage"),
    url(r"^delete/(?P<message_id>\d+)/", views.delete, name = "delete"),
    url(r"^delete_comment/(?P<comment_id>\d+)/", views.delete_comment, name = "delete_comment"),
    url(r"^edit/(?P<message_id>\d+)/", views.edit, name = "edit"),
    url(r"^update_information(?P<message_id>\d+)/", views.update_information, name = "update_information"),
    ###
    url(r"^like/(?P<message_id>\d+)/", views.like, name = "like"),
    url(r"^comment/(?P<id>\d+)/", views.comment, name = "comment"),
    url(r"^popular$", views.popular, name = "popular"),
    url(r"^popularpage$", views.popularpage, name = "popularpage"),
    url(r"^about$", views.about, name = "about"),
]
