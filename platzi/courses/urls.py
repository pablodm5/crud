from django.conf.urls import url, include
from . import views
from django.views.generic.base import TemplateView
from django_adminlte import urls
from adminlte import urls
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from .views import (
    CourseList,
    CourseDetail,
    CourseUpdate,
    CourseDelete
    )
urlpatterns = [
    url(r'^$',views.login, name='login'),
    url(r'^generar_pdf/$', views.generar_pdf, name='pdf'),
    # url(r'^pdf/', views.SimplePie, name='grafica'),
    url(r'^adminlte/', include('adminlte.urls')),
    url(r'^django_adminlte/',include('django_adminlte.urls')),
    url(r'^home/', login_required(CourseList.as_view()), name='list'),
    url(r'^(?P<pk>\d+)$', login_required(CourseDetail.as_view()), name='detail'),
    url(r'^nuevo$',login_required(views.crear), name='new'),
    url(r'^editar/(?P<pk>\d+)$', login_required(CourseUpdate.as_view()), name='edit'),
    url(r'^borrar/(?P<pk>\d+)$', login_required(CourseDelete.as_view()), name='delete'),
]
