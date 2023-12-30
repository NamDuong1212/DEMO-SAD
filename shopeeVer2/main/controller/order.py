from django.shortcuts import render, redirect
from django.contrib import messages 
from django.http.response import JsonResponse
from main.models import Cart, Product
from django.contrib.auth.decorators import login_required

from main.models import Order,OrderItem

@login_required(login_url='login')
def index(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders':orders}
    return render(request, "main/orders/index.html",context)

@login_required(login_url='login')
def vieworder(request, t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {'order':order,'orderitems':orderitems }
    return render(request, "main/orders/view.html",context)