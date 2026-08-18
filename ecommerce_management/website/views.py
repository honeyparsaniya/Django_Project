from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class IndexView(TemplateView):
    template_name="index.html"

class CartView(TemplateView):
    template_name="cart.html"

class CheackoutView(TemplateView):
    template_name="cheackout.html"

class BestsellerView(TemplateView):
    template_name="bestseller.html"


class ShopView(TemplateView):
    template_name="shop.html"

class SingleView(TemplateView):
    template_name="single.html"

