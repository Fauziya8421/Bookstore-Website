
from ast import Param
import email
from msilib.schema import _Validation
from os import remove
from statistics import quantiles
from tkinter import N
from turtle import title
from unicodedata import category
from django.shortcuts import render, HttpResponse,redirect
from django.http import HttpResponse
from numpy import true_divide
from django.contrib.auth.hashers import  check_password
from django.contrib.auth.hashers import make_password
from .models import Book , Contact,Category,Customer,Order
from math import ceil
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import json
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum

MERCHANT_KEY = 'bKMfNxPPf_QdZppa'; 

# from blog.models import Post


# Create your views here.
class Index(View):
    def post(self,request):
        book=request.POST.get('book')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(book)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(book)
                    else:    
                     cart[book]=quantity-1
                else:
                    cart[book]=quantity+1   
            else:
                cart[book]=1
        else:
            cart={}
            cart[book]=1

        request.session['cart']=cart
        print(cart)   
        return redirect('StoreHome')


    def get(self,request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}

        books=None
       
        categories=Category.get_all_categories()
        categoryID= request.GET.get('category')
        if categoryID:
            books=Book.get_all_books_by_id(categoryID) 
        else:
            books=Book.get_all_books()
        data={}
        data['books']=books
        data['categories']=categories

        thank = False
        if request.method=="POST":
            name = request.POST.get('name' , '')
            email = request.POST.get('email' , '')
            phone = request.POST.get('phone' , '')
            state = request.POST.get('state' , '')
            subject = request.POST.get('subject' , '')
            contact = Contact(name=name , email=email , phone=phone, state=state , subject=subject)
            contact.save()
            thank = True

        print('You are' ':' ,request.session.get('email'))
        data = { 'books':books ,'categories':categories,'thank': thank}
        return render(request , "store/index.html" ,data)


def basic(request):
    categories=Category.get_all_categories()
    data={}
    data['categories']=categories
    data = { 'categories':categories}
    return render(request , "store/index.html",data)



def searchMatch(query, item):
    
    query = query.lower()
    if query in item.desc.lower() or query in item.book_name.lower() or query in item.category.lower():
        return True
    else:
        return False




    


def search(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}

    query=request.GET['query']
    if len(query)>80:
        books=Book.objects.none()
    else:
        booksName=Book.objects.filter(book_name__icontains=query)
        booksDesc=Book.objects.filter(desc__icontains=query)
        books=booksName.union(booksDesc)
    data={'books':books,'query':query }
    
    return render(request,"store/search.html",data)


def about(request):
    return render(request , "store/about.html")

class Cart(View):
    
    
    def get(self,request):
        customer = request.session.get('customer')
        
        if not customer:
            ids = list(request.session.get('cart').keys())
            books = Book.get_books_by_id(ids)
            messages.error(request, " Please  loggin Before Checkout  !!!")
            return render(request , "store/cart.html"  , {'books' : books})
        else:
            ids = list(request.session.get('cart').keys())
            books = Book.get_books_by_id(ids)
            return render(request , "store/cart.html"  , {'books' : books})

def novel(request):
    return render(request , 'store/novel.html' )

def autob(request):

    return render(request , 'store/autobio.html' )



def sprit(request):
    return render(request , 'store/sprint.html' )

# def signup(request):
#     return render(request , 'store/signup.html' )


def handleSignup(request):
   if request.method =='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        customer=Customer(fname=fname,lname=lname,email=email,password=password,phone=phone)

        isExists=customer.isExists()
        if isExists:
            return HttpResponse("<h1>Email Address is Already Register</h1>")
        else:   
            customer.password = make_password(customer.password) 
            customer.register()


        return redirect('StoreHome')

        
       



        



def handleLogin(request):
    if request.method =='POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        print(email,password1)
        customer = Customer.get_customer_by_email(email)
        if customer:
            flag = check_password(password1,customer.password)
            if flag:
                request.session['customer']=customer.id
                request.session['email']=customer.email
                request.session['fname']=customer.fname
                messages.success(request, "Successfully loggin  !!!")
            else:
                messages.error(request, " invalid credencital , Please try again")
                # return HttpResponse("<h1> invalid Email OR Password</h1>")        
        else:
            messages.error(request, " invalid credencital , Please try again")
            # return HttpResponse("<h1> invalid Email OR Password</h1>")
        return redirect('StoreHome')  
        
    #     user = authenticate(username = loginusername , password =  loginpassword)

    #     if user is not None:
    #         login(request, user)
    #         messages.success(request, "Successfully logged in !!!")
    #         return redirect('StoreHome')
    #     else:
    #         messages.error(request, " invalid credencital , Please try again")
    #         return redirect('StoreHome')

        
    # return HttpResponse('404 -not found')



def handleLogout(request):
    # if request.method == 'POST':
    logout(request)
    request.session.clear()
    messages.success(request, "Successfully logged out !!!")
    return redirect('StoreHome')








def bookView(request ,myid):
    # fetch the product using the id 
    book = Book.objects.filter(id=myid)
    return render(request , 'store/books.html' , {'book':book[0]} )

# def contact(request):
#     if request.method=="POST":
#         print(request)
#     return render(request , "store/index.html" )


# def checkout(request):
#     if request.method=="POST":
#         items_json= request.POST.get('itemsJson', '')
#         name = request.POST.get('name' , '')
#         amount  = request.POST.get('amount' , '')
#         email = request.POST.get('email' , '')
#         phone = request.POST.get('phone' , '')
#         address = request.POST.get('address' , '')
#         city = request.POST.get('city' , '')
#         landmark = request.POST.get('landmark' , '')
#         district = request.POST.get('district' , '')
#         state = request.POST.get('state' , '')
#         country = request.POST.get('country' , '')
#         zip_code = request.POST.get('zip_code' , '')


#         order = Orders(items_json=items_json, name=name, amount = amount , email=email , phone=phone, address=address, city=city,landmark=landmark, district=district,  state=state , country=country,zip_code=zip_code)
#         order.save()
#         update=OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
#         update.save()
#         thank = True
#         id = order.order_id
#         # return render(request, 'store/checkout.html', {'thank':thank, 'id': id})
#         # Request pytm to generate to transfre the amount to your acount 
#                # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
#     #request paytm to transfer the amount to your account after payment by user
#         param_dict={

#                 'MID': 'DIY12386817555501617',
#                 'ORDER_ID': str(order.order_id),
#                 'TXN_AMOUNT': str(amount),
#                 'CUST_ID': email,
#                 'INDUSTRY_TYPE_ID': 'Retail',
#                 'WEBSITE': 'WEBSTAGING',
#                 'CHANNEL_ID': 'WEB',
#                 'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

#         }
#         param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)

#         return  render(request, 'store/paytm.html', {'param_dict': param_dict})
#     return render(request, 'store/checkout.html')




# @csrf_exempt
# def handlerequest(request):
#     # paytm will send you post request here
#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]

#     verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print('order successful')
#         else:
#             print('order was not successful because' + response_dict['RESPMSG'])
#     return render(request, 'store/paymentstatus.html', {'response': response_dict})

class CheckOut(View):
        def post(self, request):
            address = request.POST.get('address')
            amount = request.POST.get('amount')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            postal_code = request.POST.get('postal_code')
            state = request.POST.get('state')
            contry = request.POST.get('contry')
            customer = request.session.get('customer')
            cart = request.session.get('cart')
            books = Book.get_books_by_id(list(cart.keys()))
            print(address, phone, customer, cart, books,amount)

            for book in books:
                print(cart.get(str(book.id)))
                order = Order(customer=Customer(id=customer),
                            book=book,
                            amount=amount,
                            price=book.price,
                            email=email,
                            address=address,
                            phone=phone,
                            postal_code=postal_code,
                            state =state ,
                            contry=contry,
                            quantity=cart.get(str(book.id)))
                order.save()
            request.session['cart'] = {}
            
            # order.id
            # order_id=order.order_id,
            
           
        # request paytm to transfer the amount to your account after payment by user
            param_dict={

                'MID': 'DIY12386817555501617',
                'ORDER_ID':str(order.order_id),
                'TXN_AMOUNT':str(amount),
                'CUST_ID':email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

            }
            print(amount)
            print("amo" ,type(amount))
            print("id5",type(order.order_id))
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return  render(request, 'store/paytm.html', {'param_dict': param_dict})
            
            
            return redirect('Cart')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'store/paymentstatus.html', {'response': response_dict})
    

    
class OrderView(View):
    def get(self , request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'store/orders.html'  , {'orders' : orders})
       











