from django.conf.urls import url
from bistro import views


urlpatterns = [
    url(r'^api/bistro/test/$', views.bistromenu_test),
    url(r'^api/bistro/menus/$', views.bistromenu_list),
    url(r'^api/bistro/menus/(?P<pk>[0-9]+)$', views.bistromenu_detail)
]
