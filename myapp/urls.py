from django.urls import path
from .views import *


urlpatterns = [
    path('', Home,name='home'),
    path('about-us', About_us, name='about-us'),
    path('contact', Contact, name='contact'),
    path('tracking',TrackingPage, name='tracking'),
    path('ask',Ask,name='ask'),
    path('sawatdee',Sawatdee),
    path('question',Question,name='question'),
    path('answer/<int:askid>',Answer,name='answer'),
    path('blog/',Posts,name='posts'),
    path('blog/<slug:slug>/',PostDetail,name='post-detail'),
    #register and login
    path('register',Register,name='register'),
    path('login',Login,name='login'),
    path('products/',AllProduct,name='all_product'),
    path('discount/',DiscountPage,name='discount'),
    path('product/<slug:slug>',ProductDetail,name='product-detail'),
    path("tracking/<str:tid>/", TrackingOrderId, name="tracking-order-id-page"),
    
    #Cart
    path('add-cart/<int:pid>/', AddToCart, name='add-to-cart'),
    path('cart/',MyCart,name='my-cart'),
    path('edit-cart/', MyCartEdit , name='my-cart-edit'),
]