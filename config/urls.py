from django.contrib import admin
from django.urls import path

from dashboard import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),

    path("menu/", views.menu_list, name="menu_list"),
    
    path("inventory/", views.inventory_list, name="inventory_list"),

    path("inventory/add/", views.inventory_create, name="inventory_create"),

    path("inventory/<int:pk>/edit/", views.inventory_edit, name="inventory_edit"),

    path("inventory/<int:pk>/delete/", views.inventory_delete, name="inventory_delete"),

    path(
        "menu/add/",
        views.menu_create,
        name="menu_create"
    ),

    path(
        "menu/<int:pk>/",
        views.menu_detail,
        name="menu_detail"
    ),

    path(
        "menu/<int:pk>/edit/",
        views.menu_edit,
        name="menu_edit"
    ),

    path(
        "menu/<int:pk>/delete/",
        views.menu_delete,
        name="menu_delete"
    ),
    
    
    path("events/", views.event_list, name="event_list"),

    path("events/add/", views.event_create, name="event_create"),

    path("events/<int:pk>/", views.event_detail, name="event_detail"),

    path("events/<int:pk>/edit/", views.event_edit, name="event_edit"),

    path("events/<int:pk>/delete/", views.event_delete, name="event_delete"),

]