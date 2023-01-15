import math

from django.shortcuts import render
from django.http import HttpResponse
from . models import Product,Contact
# Create your views here.
def index(request):
    # products=Product.objects.all()
    # n=len(products)
    # nslides=math.ceil(n/4)
    # print(products)
    # print(nslides)
    # params={'product':products,'no_of_slides':nslides,'range':range(1,nslides)}
    # allProds=[[products,range(1,nslides),nslides],
    #           [products,range(1,nslides),nslides]]
    allProds=[]
    catprods=Product.objects.values('category','id')
    # print(catprods)
    cats={item['category'] for item in catprods}
    # print(cats)
    for cat in cats:
        prod=Product.objects.filter(category=cat)

        n = len(prod)
        nslides = math.ceil(n / 4)
        allProds.append([prod,range(1,nslides),nslides])
    params={'allProds':allProds}
    return render(request,'shop/index.html',params)

def about(request):
    return render(request,'shop/about.html')


def contact(request):
    if request.method=="POST":
        # print(request)
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        # print(name,email,phone,desc)
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')


def tracker(request):
    return render(request, 'shop/tracker.html')


def search(request):
    return render(request,'shop/search.html')

def productView(request,myid):
    #fetch the product using id
    product = Product.objects.filter(id=myid)
    # print(product)

    return render(request, 'shop/prodView.html',{'product':product[0]})


def checkout(request):
    return render(request, 'shop/checkout.html')

