from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import OrderPlaced, Product, Customer, Cart
from django.db.models import Count
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
 #return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        totalitems = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',locals())

class product_detail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        totalitems = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        brand = Product.objects.filter(category=val).values('brand').annotate(total=Count('brand'))
        totalitems = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/category.html',locals())

class CategoryBrandView(View):
    def get(self,request,val):
        product = Product.objects.filter(brand=val)
        brand = Product.objects.filter(category=product[0].category).values('brand').annotate(total=Count('brand'))
        totalitems = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/category.html',locals())

@login_required       
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    totalitem = len(Cart.objects.filter(user=request.user))
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 70
    return render(request,'app/addtocart.html',locals())

@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Address Updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profile.html',locals())

# def profile(request):
 #return render(request, 'app/profile.html')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'app/address.html',locals())

@login_required
def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html',locals())


def search(request):
    query = request.GET['search']
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query) | Q(brand__icontains=query) |  Q(description__icontains=query))
    return render(request,"app/search.html",locals())


def change_password(request):
        return render(request, 'app/changepassword.html')

def mobile(request):
 return render(request, 'app/mobile.html')

# def login(request):
 #return render(request, 'app/login.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        # totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Registered Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/customerregistration.html',locals())

    
@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    totalitem = len(Cart.objects.filter(user=request.user))
    amount = 0
    for p in cart_items:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 70
    return render(request, 'app/checkout.html',locals())

@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid) 
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

def plus_cart(request):
    if request.method == 'GET' :
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 70
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET' :
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 70
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data) 

def remove_cart(request):
    if request.method == 'GET' :
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 70
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)        