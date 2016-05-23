from django.conf.urls import url, include
from django.contrib.staticfiles import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
admin.autodiscover()

app_name = 'realestate'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^property/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^faq/$', views.faq_list, name='faq'),
    # url(r'^properties/$', views.properties, name='properties'),
    url(r'^search/$', views.search, name='search'),
    url(r'^controlpanel/$', views.controlpanel, name='controlpanel'),
    url(r'^disclaimer/$', views.disclaimer, name='disclaimer'),
    url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            views.reset_confirm, name='reset_confirm'),
    url(r'^reset/$', views.reset, name='reset'),
    url(r'^accountinformation/$', views.accountinformation, name='accountinformation'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'usercontrolpanel/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'usercontrolpanel/logout.html'}, name ='logout'),
    url(r'^about/$', views.about, name='about'),
    url(r'^partners/$', views.partners, name='partners'),
    url(r'^sell/$', views.sell, name='sell'),
    url(r'^rent/$', views.rent, name='rent'),
]
