from django.urls import path
from . import views

from main.controller import authview, cart, checkout, order
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register', authview.registerPage, name = 'register'),
    path('login', authview.loginPage, name = 'login'),
    path('logout', authview.logoutUser, name = 'logout'),
    path('profile', authview.profileUser, name = 'profile'),
    
    path('', views.home, name = "home"),
    path('product-list', views.productlistAjax),
    path('searchproduct', views.searchproduct, name="searchproduct"),
    
    path('product_type', views.product_type, name = 'product_type'),
    path('product_type/<str:slug>', views.product_type_view, name = 'product_type_view'),
    path('product_type/<str:cate_slug>/<str:prod_slug>', views.productview, name = "productview" ),
    
    path('password', auth_views.PasswordChangeView.as_view(template_name='main/auth/password/password_change_form.html'), name = 'password_change'),
    path('pasword_change_done', auth_views.PasswordChangeDoneView.as_view(template_name='main/auth/password/password_change_done.html'), name = 'password_change_done'),
    
    path('add-to-cart', cart.addtocart, name="addtocart" ),
    path('cart', cart.viewcart, name="cart"),
    path('update-cart', cart.updatecart, name="updatecart"),
    path('delete-cart-item', cart.deletecartitem, name="deletecartitem"),
    path('checkout', checkout.index, name="checkout"),
    path('place-order', checkout.placeorder, name="placeorder"),
    path('my-orders', order.index, name="myorders"),
    path('view-order/<str:t_no>', order.vieworder, name="orderview")
]

