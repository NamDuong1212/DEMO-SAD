from django.shortcuts import render, redirect
from django.contrib import messages
from . models import Category, Product
from django.http.response import JsonResponse

# Create your views here.
def home (request):
    trending_products = Product.objects.filter(trending = 1)
    context = {'trending_products': trending_products}
    return render(request,"main/index.html", context)

def product_type (request):
    category = Category.objects.filter(status=0)
    context = {
        'category':category
    }
    return render(request,"main/product_type.html", context)

def product_type_view(request, slug):
    if (Category.objects.filter(slug=slug, status = 0)):
        products = Product.objects.filter(category__slug = slug )
        category = Category.objects.filter(slug = slug).first()
        context = {'products' : products, 'category': category}

        return render(request, "main/products/index.html", context)
    else:
        messages.warning (request, "No category found")
        return redirect('product_type')
    
def productview(request, cate_slug, prod_slug):
    if(Category.objects.filter(slug =cate_slug, status = 0)):
        if(Product.objects.filter(slug =prod_slug, status = 0)):
            products = Product.objects.filter(slug =prod_slug, status = 0).first
            context = {'products':products}
        else:
            messages.error(request, "No such product found")
            return redirect('product_type')
    
    else:
        messages.error(request, "No such category found")
        return redirect('product_type')
    
    return render(request, 'main/products/view.html', context)

def productlistAjax(request):
    products = Product.objects.filter(status=0).values_list('name', flat=True)
    productlist = list(products)
    
    return JsonResponse(productlist, safe= False)

def searchproduct(request):
    if request.method == 'POST':
        searchedterm = request.POST.get('productsearch')
        if searchedterm =="":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains = searchedterm).first()
            
            if product:
                return redirect('product_type/' +product.category.slug +'/' +product.slug)
            else:
                messages.info(request, "No product matched your search")
                return redirect(request.META.get('HTTP_REFERER'))
        
    return redirect(request.META.get('HTTP_REFERER'))