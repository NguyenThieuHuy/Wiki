from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path("add", views.add, name="add"),
    path("note/<str:entry>", views.entry, name="entry"),
    path("note/<str:entry>/edit", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search"),
    path("delete", views.delete, name="delete"),
]
