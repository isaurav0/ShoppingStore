from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("medical", views.main_product_view, name="medical"),
    path("recreational", views.main_product_view, name="recreational"),
    path('products/my_cart_info', views.my_cart_info,
         name='my_cart_info'),
    path('products/<str:category>',
         views.product_filter, name='product_filter'),
    path('products/detail/<int:product_id>',
         views.product_detail, name='product_detail'),
    path('products/add_to_cart/<int:product_id>',
         views.add_to_cart, name='add_to_cart'),
    path('products/remove_from_cart/<int:product_id>',
         views.remove_from_cart, name='remove_from_cart'),
    path('products/<int:product_id>/add_comment',
         views.add_comment, name='add_comment'),
    path('products/comments/<int:comment_id>/comment_reply',
         views.comment_reply, name='comment_reply'),
]
