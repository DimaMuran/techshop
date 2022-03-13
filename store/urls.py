from django.urls import path

from . import views

urlpatterns = [
    path('', views.home,name='home'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('remove-cart/<int:cart_id>/', views.remove_cart, name='remove-cart'),
    path('plus-cart/<int:cart_id>/', views.plus_cart, name='plus-cart'),
    path('minus-cart/<int:cart_id>/', views.minus_cart, name='minus-cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),

    path('product/<slug:slug>/', views.detail, name='product-detail'),
    path('categories/', views.all_categories, name='all-categories'),
    path('<slug:slug>/', views.category_products, name='category-products'),

    path('accounts/register/', views.RegistrationView.as_view(), name='register'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.logoutUser, name='logout'),
]
