from unicodedata import category
from django.contrib import admin
# Register your models here.
from .models import Book , Contact,Category,Customer,Order
 


class BookAdmin(admin.ModelAdmin):
    list_display = [ 'book_name','price','category','image']

class CategoryAdmin(admin.ModelAdmin):
    list_display = [ 'name']

# class orderAdmin(admin.ModelAdmin):
#     list_display = [ 'book_name','price','category','image']
    
admin.site.register(Book,BookAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Contact)
admin.site.register(Order)
# admin.site.register(OrderUpdate)
admin.site.register(Customer)
