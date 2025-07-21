from django.shortcuts import render, HttpResponse
from .models import Category, Product
# Create your views here.
def home(request):
    return render(request, "main/base.html")
def read(request, uuid):
    product = Product.objects.get(product_id=uuid)
    return render(request, "main/read.html", {"product": product})
def list(request):
    ls = Product.objects.all()
    return render(request, "main/list.html", {"products": ls})