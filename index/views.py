from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index/home.html')

def blog(request):
    return render(request, 'index/blog.html')

def contact_us(request):
    return render(request, 'index/contact.html')
