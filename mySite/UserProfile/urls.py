from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new_user/$', views.new_user, name='new_user'),
    url(r'^editProfileInterface/$', views.editProfileInterface, name='editProfileInterface'),
    url(r'^editAlias/$', views.editAlias, name='editAlias'),
    url(r'^editUserTags/$', views.editUserTags, name='editUserTags'),
]
