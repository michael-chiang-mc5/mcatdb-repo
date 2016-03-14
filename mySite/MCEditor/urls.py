from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^editor/$', views.editor, name='editor'),
    url(r'^example/$', views.example, name='example'),
]
