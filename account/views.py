from django.shortcuts import render, HttpResponse
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
# Create your views here.
def register(request):
    form = RegisterForm()
    print("here")
    if request.method == "POST":
        print("HERE")
        form = RegisterForm(request.POST)
        print("form.is_valid(): ", form.is_valid())
        print("form.errors: ", form.errors)
        if form.is_valid():
            user_name = form.cleaned_data.get("user_name")
            password = form.cleaned_data.get("password1")
            user_type = form.cleaned_data.get("user_type")
            print("username: ", user_name)
            user = CustomUser.objects.create_user( # type: ignore
                user_name=user_name, 
                password=password, 
                user_type=user_type
            )        
            login(request, user)
            return render(request, "main/base.html")
    form = RegisterForm()
    return render(request, "account/register.html", {"form": form})
def logout_view(request):
    logout(request)
    if request.method == "POST":
        return HttpResponse("You have been logged out. <a href='/'>Go to Home</a>")
    return render(request, "account/logout.html", {"message": "You have been logged out."})