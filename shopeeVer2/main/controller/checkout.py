from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.models import *
import random
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse

@login_required(login_url='login')
def index(request):
    cart = Cart.objects.filter(user=request.user)
    for item in cart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)
        
    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.selling_price * item.product_qty
    
    userprofile = Profile.objects.filter(user=request.user).first()
        
    context ={"cartitems":cartitems, 'total_price':total_price, 'userprofile':userprofile}
    return render(request, 'main/products/checkout.html', context)

@login_required(login_url='login')
def placeorder(request):
    if request.method =="POST":
        
        currentuser = User.objects.filter(id=request.user.id).first()
        
        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()
        
        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.province = request.POST.get('province')
            userprofile.district = request.POST.get('district')
            userprofile.address = request.POST.get('address')
            userprofile.save()
        
        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.province = request.POST.get('province')
        neworder.district = request.POST.get('district')
        neworder.address = request.POST.get('address')
        
        neworder.payment_mode = request.POST.get('payment_mode')
        
        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + item.product.selling_price * item.product_qty
    
        neworder.total_price = cart_total_price
        trackno = 'Num ' + str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'Num ' + str(random.randint(1111111,9999999))
    
        neworder.tracking_no = trackno
        neworder.save()
        
        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order = neworder,
                product = item.product,
                price = item.product.selling_price,
                quantity = item.product_qty,
                
            )
            
            #Giam so luong san pham
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()
            
        #Xoa gio hang nguoi dung
        Cart.objects.filter(user=request.user).delete()
        
        messages.success(request, 'Your order has been placed successfully')
        
        payMode = request.POST.get('payment_mode')
        
        if (payMode == "Paid by PayPal"):
            return JsonResponse({'status': 'Your order has been placed successfully'})
        else:
            messages.success(request, "Your order has been placed successfully")
        
    
    return redirect('/')
    
def orders(request):
    return HttpResponse('My orders page')