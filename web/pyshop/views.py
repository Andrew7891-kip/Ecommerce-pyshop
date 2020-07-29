from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from .forms import CheckoutForm,SignUpForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    products=Product.objects.all()
    paginator = Paginator(products,8 )
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render (request,'home.html',{'page_obj': page_obj})
    

def shirt(request):
    products=Product.objects.filter(category='shirt')
    return render (request,'shirt.html',{'products':products})

def sportswear(request):
    products=Product.objects.filter(category='sportswear')
    return render (request,'sportswear.html',{'products':products})

def outwear(request):
    products=Product.objects.filter(category='outwear')
    return render (request,'outwear.html',{'products':products})

def product(request,slug):
    prod=Product.objects.get(slug=slug)
    return render (request,'product.html',{'prod':prod})

@login_required
def add_to_cart(request,slug):
    item=Product.objects.get(slug=slug)
    order_item,created=Cart.objects.get_or_create(
        item=item,
        user=request.user
    )
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,f" {item.name} was updated")
            return redirect('product' ,item.slug )
        else:
            order.orderitems.add(order_item)
            messages.info(request,f" {item.name} was added to your cart")
            return redirect('product' ,item.slug )
    else:
        order=Order.objects.create(
            user=request.user
        )
        order.orderitems.add(order_item)
        messages.info(request,f" {item.name} was added to your cart")
        return redirect('product', item.slug )

def remove_from_cart(request,slug):
    item=Product.objects.get(slug=slug)
    cart_qs=Cart.objects.filter(
        user=request.user,
        item=item
    )
    if cart_qs.exists():
        cart=cart_qs[0]
        if cart.quantity > 1:
            cart.quantity -=1
            cart.save()
        else:
            cart_qs.delete()
    
    order_qs=Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order=order_qs[0]
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item=Cart.objects.filter(
                user=request.user,
                item=item
            )[0]
            order.orderitems.remove(order_item)
            messages.info(request,f" {item.name} was removed from your cart ")
            return redirect('product' ,item.slug)
        else:
            messages.info(request,f" {item.name} was not in your cart ")
            return redirect('product' ,item.slug)
    else:
        messages.info(request,"You don't have an active order")
        return redirect('product', item.slug)



def cart(request):
    user=request.user
    carts=Cart.objects.filter(user=user)
    orders=Order.objects.filter(user=user,ordered=False)
    if carts.exists():
        order=orders[0]
        return render (request,'cart.html',{'carts':carts,'order':order})
    else:
        messages.info(request,'You do not have an active order')
        return redirect('home'  )

def update_add(request,slug):
    item=Product.objects.get(slug=slug)
    order_item,created=Cart.objects.get_or_create(
        item=item,
        user=request.user
    )
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,f" {item.name} was updated")
            return redirect('cart' )
        else:
            order.orderitems.add(order_item)
            messages.info(request,f" {item.name} was added to your cart")
            return redirect('cart')
    else:
        order=Order.objects.create(
            user=request.user
        )
        order.orderitems.add(order_item)
        messages.info(request,f" {item.name} was added to your cart")
        return redirect('cart' )

        

def update_remove(request, slug):
    item = Product.objects.get(slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
            messages.info(request, f"{item.name} quantity has updated.")
            return redirect("cart")
        else:
            messages.info(request, f"{item.name} quantity has updated.")
            return redirect("cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("home")
    
def checkout(request):
    if request.method == 'POST':
        form=CheckoutForm(request.POST)
        orders=Order.objects.filter(user=request.user,ordered=False)
        if form.is_valid():
            address=form.cleaned_data.get('address')
            county=form.cleaned_data.get('county')
            country=form.cleaned_data.get('country')
            #TODO
            # same_billing_address=form.cleaned_data.get('same_billing_address')
            # save_info=form.cleaned_data.get('save_info')
            payment_option=form.cleaned_data.get('payment_option')
            billing_address=Checkout(
                user=request.user,
                county=county,
                country=country,
                address=address
            )
            billing_address.save()
            orders.billing_address=billing_address
            # orders.save()
            messages.success(request,'Checked out successfully')
            return redirect('/')
    else:
       form=CheckoutForm() 
    #    messages.warning(request,'Checkout failed, Try again!')
    return render (request,'checkout.html',{'form':form})
    

def signup(request):
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render (request,'signup.html',{'form':form})