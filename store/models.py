from distutils.command.upload import upload
import email,datetime
from email.mime import image
from email.policy import default
from re import M
from tkinter import N
from unicodedata import category, name
from django.db import models


    

# Create your models here.
class Book(models.Model):
    book_id = models.AutoField
    book_name = models.CharField(max_length=50)
    category=models.ForeignKey('Category',on_delete=models.CASCADE, default=0)
    desc = models.CharField(max_length=5000)
    price = models.IntegerField(default=0)
    pub_date = models.DateField()
    image = models.ImageField(upload_to = "store/images" , default="")
    
    
    def __str__(self) :
        return self.book_name

    @staticmethod
    def get_books_by_id(ids):
        return Book.objects.filter(id__in =ids)    
    
    @staticmethod
    def get_all_books_by_id(category_id):
        if category_id:
            return Book.objects.filter(category=category_id)  
        else:
            return Book.get_all_books()

    @staticmethod
    def get_all_books():
        return Book.objects.all()



class Category(models.Model):
    name=models.CharField(max_length=20)

    @staticmethod
    def  get_all_categories():
       return Category.objects.all()

   

    
    def __str__(self) :
        return self.name

# Create your 2 models here.
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    email = models.CharField(max_length=40 )
    phone = models.CharField(max_length=10)
    state = models.CharField(max_length=40)
    subject = models.CharField(max_length=5000)
   

    def __str__(self) :
        return self.name

# Create your order models here.


# class OrderUpdate(models.Model):
#     update_id =models.AutoField(primary_key=True)
#     order_id =models.IntegerField(default="")
#     update_desc=models.CharField( max_length=5000)
#     timestamp=models.DateField(auto_now_add=True)

#     def _str_(self):
#         return self.update_desc[0.7] +"....."


class Customer(models.Model):
    fname = models.CharField(max_length=90)
    lname = models.CharField(max_length=90)
    email = models.CharField(max_length=40)
    phone = models.EmailField(max_length=10)
    password = models.CharField(max_length=10)


    def __str__(self) :
        return self.fname

    def register(self):
        self.save()

    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return  False

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False


# Create your order models here.
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    email = models.CharField(max_length=40)
    address = models.CharField(max_length=50, default='')
    postal_code = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50, default='')
    contry = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=50, default='')
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    amount=models.ImageField(default=0)

    def Order(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
      return  Order.objects.filter(customer=customer_id).order_by('-date')

    @staticmethod
    def total(amount):
        if amount==0:
            return amount==('books|total_cart_price:request.session.cart|currency')
        else:
            return amount

           