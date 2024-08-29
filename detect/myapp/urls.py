from django.urls import path
from . views import login_, register, dashboard, product_setup, logout_view, get_product_info

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', login_, name="login"),
    path('', dashboard, name="dashboard"),
    path('product_setup/<str:pk>/', product_setup, name="product_setup"),
    path('get_product_info/<str:pk>/', get_product_info, name="get_product_info"),
    path('logout_view/', logout_view, name="logout"),
]