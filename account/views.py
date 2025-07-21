from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
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
            print("SAVED: ", form.cleaned_data)
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, "main/base.html")
    form = RegisterForm()
    return render(request, "account/register.html", {"form": form})