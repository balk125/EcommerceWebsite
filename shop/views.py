from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import product,Contact,orders,orderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login

# Create your views here.
MERCHANT_KEY = 'A5OlxmCou7VL9t2f'



def signup( request):
    if request.method=="POST":
        # username=request.POST.get('username')
        username=request.POST.get('username')
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        confirmPassword=request.POST.get('confirmPassword')
        gender=request.POST.get('gender')
        

        myuser=User.objects.create_user(username,email,password)
        myuser.full_name=name
        myuser.save()

        messages.success(request,"your registration has been successfully created")

        return redirect('signin')
    return render(request,'shop/signup.html')


def signin( request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)

            allProds=[]
            catprods=product.objects.values('category','id')
            cats={item['category'] for item in catprods}
            for cat in cats:
                prod=product.objects.filter(category=cat)
                n=len(prod)
                nSlides=n//4 + ceil((n/4)-(n//4))
                allProds.append([prod,range(1,nSlides ),nSlides])

            params={'allProds':allProds,'username':username,'logout':'logout'}
            return render(request,'shop/index.html',params)

        else:
            
            return render(request,'shop/signin.html',{'error_msg':"Wrong username or password"})



    return render(request,'shop/signin.html')


def signout(request):
    pass




 



def index(request):
    # products=product.objects.all()
    # print(products)
    # n=len(products)
    # nSlides=n//4 + ceil((n/4)-(n//4))
    # params={'no_of_Slides':nSlides,'product':products,'range':range(1,nSlides)}
    # allProds=[[products,range(1,nSlides),nSlides],
    # [products,range(1,nSlides),nSlides]]
    allProds=[]
    catprods=product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=product.objects.filter(category=cat)
        n=len(prod)
        nSlides=n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides ),nSlides])

    params={'allProds':allProds}
    return render(request,'shop/index.html',params)



def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods  = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod =[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)

   
def searchMatch(query, item):
    if query in item.product_name or query in item.category:
        return True
    else:
        return False





def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method=="POST":
        # print(request)
        name= request.POST.get('name','')
        email= request.POST.get('email','')
        phone= request.POST.get('phone','')
        desc= request.POST.get('desc','')
        thank=True
        # print(name,email,phone,desc)
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        return render(request,'shop/contact.html',{'thank':thank})  
       

    return render(request,'shop/contact.html')


  
def tracker(request):
    if request.method=="POST":
        orderId= request.POST.get('orderId','')
        email= request.POST.get('email','')
        try:
            order=orders.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update=orderUpdate.objects.filter(order_id=orderId)
                updates=[]
                for item in update:

                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response=json.dumps( [ updates, order[0].items_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')


    return render(request,'shop/tracker.html')




def prodView(request,id):
    
    #Fetch the product using the id
    prod=product.objects.filter(id=id)
    return render(request,'shop/productview.html',{'product':prod[0]})


def checkout(request):
    if request.method=="POST":

        items_json= request.POST.get('itemsJson','')
        name= request.POST.get('name','')
        amount= request.POST.get('amount','')
        email= request.POST.get('email','')
        phone= request.POST.get('phone','')
        address= request.POST.get('address1','') + " " + request.POST.get('address2','')
        city= request.POST.get('city','')
        state= request.POST.get('state','')
        zip_code= request.POST.get('zip_code','')
        ordr=orders(items_json=items_json,name=name,email=email,phone=phone,address=address, city=city, state=state,zip_code=zip_code,amount=amount)
        ordr.save()
        
        update =orderUpdate(order_id=ordr.order_id,update_desc="The order has been placed Successfully")
        update.save()
        
        # ordr=orders(order_id_view=update.order_id)

        thank=True
        id=ordr.order_id
        # return render(request,'shop/checkout.html',{'thank':thank,'id':id})
        # request paytm to transfer the amount after payment by user
        
        param_dict={

            'MID': 'dSKIwb65634219318687',
            'ORDER_ID': str(ordr.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': 'email',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

        
        # return  render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, 'shop/checkout.html')
        
       
@csrf_exempt
def handlerequest(request):
    form=request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i]=form[i]
        if i=='CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})

    # return HttpResponse('this is payment page')


