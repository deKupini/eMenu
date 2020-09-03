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
    url(
        r'^api/v1/menu_list/$',
        views.MenuCardList.as_view(),
        name='menu_card_list'
    ),
    url(
        r'^api/v1/menu_detail/(?P<pk>[0-9]+)$',
        views.MenuCardDetail.as_view(),
        name='menu_card_detail'
    ),
]
