from django.urls import path
from . import views
urlpatterns = [
    path("test_json_view/", views.test_json_view, name="test_json_view"),
    path('post_json_view/', views.post_json_view, name='post_json_view'),
    path('products/', views.get_all_products, name='get_all_products'),
    path('products/most_expensive/', views.get_most_expensive_product, name='get_most_expensive'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/update/<int:pk>/', views.update_product, name='update_product'),

]