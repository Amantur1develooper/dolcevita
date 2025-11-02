# menu/urls.py
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:product_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/checkout/", views.checkout_whatsapp, name="checkout"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("contacts/", views.contacts, name="contacts"),  # ← новинка
     path("about/", views.about, name="about"), 
]
