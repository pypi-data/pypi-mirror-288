from django.urls import path
from .views import app_view, shopify_view

urlpatterns = [
    path('', shopify_view),
    path('app/', app_view),
]