from django.urls import path
from .views import *
urlpatterns = [
   path("",IndexView.as_view(),name="index_page"),
   path("cart/",CartView.as_view(),name="cart_page"),
   path("checkout/",CheackoutView.as_view(),name="checkout_page"),
   path("bestseller/",BestsellerView.as_view(),name="bestseller_page"),
   path("shop/",ShopView.as_view(),name="shop_page"),
   path("single/",SingleView.as_view(),name="single_page")
]

