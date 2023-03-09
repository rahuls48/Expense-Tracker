from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("edit/<int:id>/", views.edit, name='edit'), # /edit/1/ gives you the edit form of the first expense
    path("delete/<int:id>/", views.delete, name='delete'),
]
