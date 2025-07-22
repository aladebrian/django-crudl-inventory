from django.utils import timezone
from django.shortcuts import render, HttpResponse
from .models import Category, Product, next_category_id

def home(request):
    return render(request, "main/base.html")

def read(request, uuid):
    product = Product.objects.get(product_id=uuid)
    return render(request, "main/read.html", {"product": product})

def list(request, num=1):
    ls = Product.objects.all()
    return render(request, "main/list.html", {"products": ls})

def create(request):
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to create a product.")
    if request.user.user_type == "customer":
        return HttpResponse("Customers cannot create products.")
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        category_name = request.POST.get("category_name")
        category = Category.objects.filter(name=category_name).first()
        if not category:
            category_description = request.POST.get("category_description")
            category = Category.objects.create(
                category_id=next_category_id(), 
                name=category_name, 
                description=category_description
            )
        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category_id=category,
            seller_id=request.user
        )
        return HttpResponse(f"Product {product.name} created successfully!")
    
    categories = Category.objects.all()
    return render(request, "main/product_form.html", {"categories": categories})

def update(request, uuid=None):
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to update a product.")
    if uuid is None:
        products = Product.objects.filter(seller_id=request.user)
        return render(request, "main/update_list.html", {"products": products})
    product = Product.objects.get(product_id=uuid)
    if request.user != product.seller_id:
        return HttpResponse("You can only update products you own.")
    if request.method == "POST":
        product.name = request.POST.get("name", product.name)
        product.description = request.POST.get("description", product.description)
        product.price = request.POST.get("price", product.price)
        product.quantity = request.POST.get("quantity", product.quantity)
        category_name = request.POST.get("category_name")
        category = Category.objects.filter(name=category_name).first()
        if not category:
            category_description = request.POST.get("category_description")
            category = Category.objects.create(
                category_id=next_category_id(), 
                name=category_name, 
                description=category_description
            )
        product.category_id = category
        product.updated_at = timezone.now()
        product.save()
        return HttpResponse(f"Product {product.name} updated successfully!")
    categories = Category.objects.all()
    return render(request, "main/product_form.html", {"categories": categories, "product": product})

def deleteProduct(request, uuid=None):
    
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to delete a product.")
    
    if uuid is None:
        products = Product.objects.filter(seller_id=request.user)
        return render(request, "main/delete_list.html", {"products": products})
    product = Product.objects.get(product_id=uuid)
    if request.user != product.seller_id or not request.user.is_staff:
        return HttpResponse("You can only delete products you own.")
    if request.method == "POST":
        if request.POST.get("product_name") != product.name:
            return HttpResponse("Product deletion cancelled.")
        product.delete()
    return render(request, "main/delete_product.html", {"product": product})