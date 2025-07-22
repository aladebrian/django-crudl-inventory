from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("read/<uuid:uuid>", views.read, name="read"),
    path("list/", views.list, name="list"),
    path("list/page<int:num>", views.list, name="list"),
    path("create/", views.create, name="create"),
    path("update/", views.update, name="update"),
    path("update/<uuid:uuid>", views.update, name="update"),
    path("delete/", views.deleteProduct, name="delete"),
    path("delete/<uuid:uuid>", views.deleteProduct, name="delete"),
]