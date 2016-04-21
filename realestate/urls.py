from django.conf.urls import url,include
from django.contrib.staticfiles import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
admin.autodiscover()

app_name = 'realestate'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^faq/$', views.faq_list, name='faq'),
    url(r'^controlpanel/$', views.controlpanel, name='controlpanel'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'usercontrolpanel/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'usercontrolpanel/logout.html'}, name ='logout'),
	url(r'^info/$', views.algemene_info, name='info'),
]
