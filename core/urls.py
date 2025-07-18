from django.urls import path
from . import views


app_name = 'core'


urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('profile/', views.profile_view, name='profile'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/multi/', views.multi_checkout, name='multi_checkout'),
    path('verify/', views.verify_payment, name='verify_payment'),
    path('account/', views.account_view, name='account'),  # ✅ define this

]
