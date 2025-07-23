from django.utils import timezone
from django.shortcuts import render, HttpResponse
from account.models import CustomUser
from .models import Category, Product, next_category_id
from django.core.paginator import Paginator
def home(request, extraContent=""):
    return render(request, "main/base.html", {"extraContent": extraContent})

def read(request, uuid):
    product = Product.objects.get(product_id=uuid)
    return render(request, "main/read.html", {"product": product})

def list(request):
    p = Paginator(Product.objects.all(), 5)
    page = request.GET.get("page")
    products = p.get_page(page)

    return render(request, "main/list.html", {"products": products})

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
        return home(request, extraContent=f"Product {product.name} created successfully!")
    
    categories = Category.objects.all()
    return render(request, "main/product_form.html", {"categories": categories})

def update(request, uuid=None):
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to update a product.")
    if uuid is None:
        if request.user.user_type == "admin":
            products = Product.objects.all()
        else:
            products = Product.objects.filter(seller_id=request.user)
        return render(request, "main/update_list.html", {"products": products})
    product = Product.objects.get(product_id=uuid)
    if request.user != product.seller_id and not request.user.user_type == "admin":
        return HttpResponse("You can only update products you own.")
    if request.method == "POST":
        update_fields = ["name", "description", "price", "quantity", "updated_at", "category_id"]
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.quantity = request.POST.get("quantity")
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
        product.save(update_fields=update_fields)
        return home(request, extraContent=f"Product {product.name} updated successfully!")
    categories = Category.objects.all()
    return render(request, "main/product_form.html", {"categories": categories, "product": product})

def delete_product(request, uuid=None):
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to delete a product.")
    if uuid is None:
        if request.user.user_type == "admin":
            products = Product.objects.all()
        else:
            products = Product.objects.filter(seller_id=request.user)
        return render(request, "main/delete_list.html", {"products": products})
    product = Product.objects.get(product_id=uuid)
    if request.user.user_type == "customer":
        return HttpResponse("Customers cannot delete products.")
    if request.user != product.seller_id and not request.user.user_type == "admin":
        return HttpResponse("You can only delete products you own.")
    if request.method == "POST":
        if request.POST.get("product_name") != product.name:
            return render(request, "main/delete_product.html", {
                "product": product,
                "error": "Product name does not match. Please try again."
            })
        name = product.name
        product.delete()
        return home(request, extraContent=f"Product {name} deleted successfully!")
    return render(request, "main/delete_product.html", {"product": product})

def delete_user(request, user_id=None):
    if not request.user.is_authenticated or not request.user.user_type == "admin":
        return HttpResponse("You must be an admin to delete users.")
    if user_id is None:
        users = CustomUser.objects.exclude(user_type='admin')
        return render(request, "main/delete_user_list.html", {"users": users})
    user = CustomUser.objects.get(user_id=user_id)
    products = Product.objects.filter(seller_id=user)
    if not user:
        return render(request, "main/delete_user.html", {"error": "User not found."})
    if request.method == "POST":
        print("here")
        if request.POST.get("confirmation") != "yes":
            return render(request, "main/delete_user.html", {
                "problem_user": user,
                "error": "You must confirm deletion by typing 'yes'."
            })
        user.delete()
        return home(request, extraContent=f"User {user.user_name} deleted successfully!")
    return render(request, "main/delete_user.html", {"problem_user": user, "products": products})