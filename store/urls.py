from django.contrib import admin
from django.urls import path
from .import views
from  .views import Index,Cart,CheckOut,OrderView
# from .views.orders import OrderView
from store.middlewares.auth import auth_middleware



urlpatterns = [
    # path("", views.index , name="StoreHome"),
    path("", Index.as_view() , name="StoreHome"),
    path("cart/", Cart.as_view() , name="Cart"),
    path("about/", views.about , name="AboutUs"),
    path("novel/", views.novel , name="Novels"),
    path("autob/", views.autob , name="Autobiography"),
   
    path("sprit/", views.sprit , name="Sprituality"),
    path("search/",views.search , name="Search"),
    path("books/<int:myid>", views.bookView , name="BookView"),
    path("signup/", views.handleSignup , name="handleSignup "),
    path("login/", views.handleLogin , name="handleLogin"),
    path("logout/", views.handleLogout , name="handleLogout"),
    path('check-out', CheckOut.as_view() , name='checkout'),
    # path("orders/", Order.as_view(), name='orders'),
    path("orders/",auth_middleware(OrderView.as_view()), name='orders'),
  
    path("handlerequest/", views.handlerequest , name="HandleRequest "),
    
    
]