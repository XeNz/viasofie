from django.conf.urls import url
from django.contrib.staticfiles import views

from . import views

app_name = 'realestate'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^faq/$', views.Faqview.as_view(), name='faq'),
]
