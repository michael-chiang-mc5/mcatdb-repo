from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin_questionOfTheDay/$', views.admin_questionOfTheDay, name='admin_questionOfTheDay'),
    url(r'^adminOptions_questionOfTheDay/$', views.adminOptions_questionOfTheDay, name='adminOptions_questionOfTheDay'),
    url(r'^about/$', views.about, name='about'),
    url(r'^questionOfTheDay/$', views.questionOfTheDay, name='questionOfTheDay'),


]
