from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("read/<uuid:uuid>", views.read, name="read"),
    path("list/", views.list, name="list"),
    path("create/", views.create, name="create"),
]