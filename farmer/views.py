from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from site_admin.models import *
from django.core.files.storage import FileSystemStorage

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
                    request.session['usertype'] = 'farmer_user'
                    return redirect(reverse('farmer:dashboard'))
                else:
                    messages.error(request, 'User is suspended. Contact the admin!')
                    return redirect(reverse('farmer:signin'))
            else:
                messages.error(request, 'Invalid credentials!')
                return redirect(reverse('farmer:signin'))
    return render(request,'farmer/signin.html')

def signup(request):
    if request.method == 'POST':
        data_record = request.POST
        if Registration.objects.filter(email=data_record['email_address']):
            messages.error(request, 'Email already exists! Please try again!')
            return redirect(reverse('farmer:signup'))
        elif Registration.objects.filter(mobilenumber=data_record['mobilenumber']):
            messages.error(request, 'Mobile number already exists! Please try again!')
            return redirect(reverse('farmer:signup'))
        else:
            registration = Registration(
            firstname=data_record['firstname'],
            lastname=data_record['lastname'],
            email=data_record['email_address'],
            mobilenumber=data_record['mobilenumber'],
            address=data_record['address'],
            password=data_record['password'],
            location=Location.objects.filter(unique_id=data_record['location_list']).get(),
            status='active',
            )
            registration.save()
            messages.success(request, 'Farmer user registered successfully!')
            return redirect(reverse('farmer:signin'))
    loaction_list = Location.objects.all()
    context = { 'loaction_list' : loaction_list }
    return render(request,'farmer/signup.html', context)

def logout(request):
    del request.session['is_logged_in']
    del request.session['firstname']
    del request.session['lastname']
    del request.session['email']
    del request.session['user_id']
    del request.session['mobilenumber']
    del request.session['usertype']
    return redirect(reverse('farmer:signin'))

def dashboard(request):
    return render(request,'farmer/dashboard.html')

def products_list(request):
    product_list = Products.objects.all()
    context = { 'product_list' : product_list }
    return render(request,'farmer/list-products.html', context)

def products_add(request):
    if request.method == 'POST':
        data_record = request.POST
        uploaded_file = request.FILES['change_avatar']
        fs = FileSystemStorage()
        file_name = fs.save("PRODUCTS_"+uploaded_file.name, uploaded_file)
        products = Products(
        title=data_record['title'],
        price=data_record['price'],
        text=data_record['title_text'],
        description=data_record['description'],
        weight=data_record['weight'],
        availability=data_record['availability'],
        category=Category.objects.filter(unique_id=data_record['category_list']).get(),
        product_image=fs.url(file_name),
        )
        products.save()
        messages.success(request, 'Products added successfully!')
        return redirect(reverse('farmer:products_list'))
    category_list = Category.objects.all()
    context = { 'category_list' : category_list }
    return render(request,'farmer/add-products.html', context)

def delete_products(request, id):
    Products.objects.filter(unique_id=id).delete()
    messages.error(request, 'Product deleted successfully!')
    return redirect(reverse('farmer:products_list'))

def products_view(request, id):
    products = Products.objects.get(unique_id=id)
    if request.method == 'POST':
        data_record = request.POST
        products.title = data_record['title']
        products.price = data_record['price']
        products.text = data_record['title_text']
        products.description = data_record['description']
        products.weight = data_record['weight']
        products.availability = data_record['availability']
        products.category = Category.objects.get(unique_id=data_record['category_list'])
        products.save()
        messages.success(request, 'Products updated successfully!')
        return redirect(reverse('farmer:products_view', args=[id] ))
    category_list = Category.objects.all()
    context = { 'category_list' : category_list, 'products_data' : products }
    return render(request,'farmer/view-products.html', context)
