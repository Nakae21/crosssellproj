from django.contrib import admin
from django.urls import path, include
from core.views import product_list  # Import the product_list view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", product_list, name="home"),  # Root URL -> product_list
    path("", include("core.urls")),  # Keep this for namespaced URLs if needed
]
