from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from public.models import Registration as User_Registration
from farmer.models import Registration as Farmer_Registration, Products

# Create your views here.
def login(request):
    if request.method == 'POST':
        data_record = request.POST
        if data_record['email'] == 'admin@admin.com' and data_record['password']  == 'admin':
            request.session['is_logged_in'] = True
            request.session['email'] = 'admin@admin.com'
            request.session['full_name'] = 'admin'
            request.session['usertype'] = 'admin'
            messages.success(request, 'Logged in as admin!')
            return redirect(reverse('site_admin:dashboard'))
        else:
            messages.error(request, 'Wrong credentials. Try again!')
            return redirect(reverse('site_admin:login'))
    return render(request,'site_admin/signin.html')

def logout(request):
    del request.session['is_logged_in']
    del request.session['email']
    del request.session['usertype']
    return redirect(reverse('index:home'))

def dashboard(request):
    return render(request,'site_admin/dashboard.html')

def add_location(request):
    if request.method == 'POST':
        data_record = request.POST
        location = Location(
        location = data_record['location']
        )
        location.save()
        messages.success(request, 'Location added successfully!')
        return redirect(reverse('site_admin:add_location'))
    location_list = Location.objects.all()
    context = { 'location_list' : location_list }
    return render(request,'site_admin/add-location.html', context)

def delete_location(request, id):
    Location.objects.filter(unique_id=id).delete()
    messages.error(request, 'Location deleted successfully!')
    return redirect(reverse('site_admin:add_location'))

def add_category(request):
    if request.method == 'POST':
        data_record = request.POST
        check_category_exists = Category.objects.filter(category_name=data_record['category_name']).all()
        if check_category_exists:
            messages.error(request, 'Category already exists. Try another!')
        else:
            category = Category(
            category_name = data_record['category_name'],
            )
            category.save()
            messages.success(request, 'Category added successfully!')
        return redirect(reverse('site_admin:add_category'))
    category_list = Category.objects.all()
    context = { 'category_list': category_list }
    return render(request,'site_admin/add-category.html', context)

def delete_category(request, id):
    Category.objects.filter(unique_id=id).delete()
    messages.error(request, 'Category deleted successfully!')
    return redirect(reverse('site_admin:add_category'))

def list_public_user(request):
    datalist = User_Registration.objects.all()
    context = { 'datalist': datalist }
    return render(request,'site_admin/list-public-user.html', context)

def list_farmer_user(request):
    datalist = Farmer_Registration.objects.all()
    context = { 'datalist': datalist }
    return render(request,'site_admin/list-farmer-user.html', context)

def list_products(request):
    datalist = Products.objects.all()
    context = { 'datalist': datalist }
    return render(request,'site_admin/list-products.html', context)
