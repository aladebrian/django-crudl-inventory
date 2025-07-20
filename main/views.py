from django.shortcuts import render, HttpResponse
from .models import User, Category, Product
# Create your views here.
def home(request):
    return render(request, "base.html")

def list(request):
    ls = Product.objects.all()
    return render(request, "list.html", {"products": ls})