from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from farmer.models import Registration as Farmer_Registration, Products as Farmer_Products
from site_admin.models import Category as Admin_Category
# Create your views here.
def signin(request):
    if request.method == 'POST':
            data_record = request.POST
            if Registration.objects.filter(mobilenumber=data_record['mobilenumber'],password=data_record['password']):
                user_details = Registration.objects.get(mobilenumber=data_record['mobilenumber'],password=data_record['password'])
                if user_details.status == 'active':
                    request.session['is_logged_in'] = True
                    request.session['email'] = user_details.email
                    request.session['firstname'] = user_details.firstname
                    request.session['lastname'] = user_details.lastname
                    request.session['user_id'] = user_details.unique_id
                    request.session['mobilenumber'] = user_details.mobilenumber
                    request.session['usertype'] = 'user'
                    return redirect(reverse('public:dashboard'))
                else:
                    messages.error(request, 'User is suspended. Contact the admin!')
                    return redirect(reverse('public:signin'))
            else:
                messages.error(request, 'Invalid credentials!')
                return redirect(reverse('public:signin'))
    return render(request,'public/signin.html')

def signup(request):
    if request.method == 'POST':
        data_record = request.POST
        if Registration.objects.filter(email=data_record['email_address']):
            messages.error(request, 'Email already exists! Please try again!')
            return redirect(reverse('public:signup'))
        elif Registration.objects.filter(mobilenumber=data_record['mobilenumber']):
            messages.error(request, 'Mobile number already exists! Please try again!')
            return redirect(reverse('public:signup'))
        else:
            registration = Registration(
            firstname=data_record['firstname'],
            lastname=data_record['lastname'],
            email=data_record['email_address'],
            mobilenumber=data_record['mobilenumber'],
            address=data_record['address'],
            password=data_record['password'],
            status='active',
            )
            registration.save()
            messages.success(request, 'public user registered successfully!')
            return redirect(reverse('public:signin'))
    return render(request,'public/signup.html')

def logout(request):
    del request.session['is_logged_in']
    del request.session['firstname']
    del request.session['lastname']
    del request.session['email']
    del request.session['user_id']
    del request.session['mobilenumber']
    del request.session['usertype']
    return redirect(reverse('public:signin'))

def dashboard(request):
    return render(request,'public/dashboard.html')

def header_search_item(request):
    return redirect(reverse('public:shop'))

def shop(request):
    categories = Admin_Category.objects.all()
    #latest_products = Farmer_Products.objects.all().order_by('date_added')[:9]
    products = Farmer_Products.objects.all()
    context = { 'categories':categories, 'products':products }
    return render(request,'public/shop.html', context)

def shop_details(request, id):
    products = Farmer_Products.objects.get(unique_id=id)
    if request.method == 'POST':
        data_record = request.POST
        if 'is_logged_in' not in request.session:
           messages.error(request, 'You must sign in to buy the product!')
           return redirect(reverse('public:signin'))        
        shopping_cart = ShoppingCart(
            public_user = Registration.objects.get(unique_id=request.session['user_id']),
            products = Farmer_Products.objects.get(unique_id=id),
            quantity = data_record['quantity'],
            )
        shopping_cart.save()
        messages.success(request, 'Item added to cart!')
        return redirect(reverse('public:shop_cart'))
    context = { 'products':products }
    return render(request,'public/shop-details.html', context)

def shop_cart(request):
    if 'is_logged_in' not in request.session:
      messages.error(request, 'You must sign in to buy the product!')
      return redirect(reverse('public:signin'))
    cart_list = ShoppingCart.objects.filter(public_user=Registration.objects.get(unique_id=request.session['user_id'])).all()
    total_price = 0;
    for row in cart_list:
        total_price = total_price + (row.quantity * row.products.price)
    context = { 'cart_list':cart_list, 'total_price': total_price }
    return render(request,'public/shop-cart.html', context)

def shop_cart_delete(request, id):
    ShoppingCart.objects.filter(unique_id=id).delete()
    messages.error(request, 'Item deleted to cart!')
    return redirect(reverse('public:shop_cart'))

def shop_checkout(request):
    if request.method == 'POST':
        data_record = request.POST
        return redirect(reverse('public:shop_checkout_order'))
    cart_list = ShoppingCart.objects.filter(public_user=Registration.objects.get(unique_id=request.session['user_id'])).all()
    total_price = 0;
    for row in cart_list:
        total_price = total_price + (row.quantity * row.products.price)
    context = { 'cart_list':cart_list, 'total_price': total_price }
    return render(request,'public/shop-checkout.html', context)

def shop_checkout_order(request):
    ShoppingCart.objects.filter(public_user=Registration.objects.get(unique_id=request.session['user_id'])).delete()
    return render(request,'public/shop-checkout-order.html')
