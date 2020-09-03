from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^api/v1/dish/$',
        views.create_dish,
        name='create_dish'
    ),
    url(
        r'^api/v1/dish/(?P<pk>[0-9]+)$',
        views.modify_dish,
        name='modify_dish'
    ),
    url(
        r'^api/v1/menu/$',
        views.create_menu_card,
        name='create_menu_card'
    ),
    url(
        r'^api/v1/menu/(?P<pk>[0-9]+)$',
        views.modify_menu_card,
        name='modify_menu_card'
    ),
]
