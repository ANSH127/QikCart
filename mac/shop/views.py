import math
import json
from django.shortcuts import render
from django.http import HttpResponse
from . models import Product,Contact,Orders,OrderUpdate
import datetime

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
        status=True
        return render(request, 'shop/contact.html',{'status':status})

    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        orderid = request.POST.get('orderid', '')
        email = request.POST.get('email', '')

        try:
            order=Orders.objects.filter(order_id=orderid,email=email)
            if len(order)>0:
                Update=OrderUpdate.objects.filter(order_id=orderid)
                updates=[]
                def timeformat(value,value2):
                    value=str(value)
                    value2=str(value2)
                    yy=value[:4]
                    mm=value[5:7]
                    dd=value[8:]
                    TT=value2[:8]
                    # print(TT)
                    x=datetime.datetime(int(yy),int(mm),int(dd))
                    return(x.strftime("%a %b %d %Y")+" "+TT)

                for item in Update:
                    # timeformat(item.timestamp,item.timefield)
                    # print(item.timefield)
                    updates.append({'text':item.update_desc,'time':timeformat(item.timestamp,item.timefield)})
                    response=json.dumps([updates,order[0].items_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def search(request):
    return render(request,'shop/search.html')

def productView(request,myid):
    #fetch the product using id
    product = Product.objects.filter(id=myid)
    # print(product)

    return render(request, 'shop/prodView.html',{'product':product[0]})


def checkout(request):
    if request.method == "POST":
        # print(request)
        item=request.POST.get('itemsJson','')
        name = request.POST.get('name', '')
        lname = request.POST.get('lname', '')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        phone = request.POST.get('phone', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        # print(name,email,phone,desc)
        order = Orders(items_json=item,name=name,lname=lname, email=email, phone=phone,address=address1,
                       address2=address2,city=city,state=state,zip_code=zip_code)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="The order has been placed")
        update.save()
        thank=True
        id=order.order_id
        return render(request, 'shop/checkout.html',{'thank':thank,'id':id})
    return render(request, 'shop/checkout.html')

