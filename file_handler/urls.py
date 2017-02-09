from django.conf.urls import url

from . import views

urlpatterns = [
    url('^list/$', views.ListView.as_view(), name='list'),
    url('^import/$', views.ImportView.as_view(), name='import'),
    url('^access/(?P<pk>\d+)/$', views.AccessView.as_view(), name='access'),
    url('^datasets/$', views.DatasetView.as_view(), name='dataset'),
    url('^add_feature/$', views.AddFeatureView.as_view(), name='add_feature')
]
