from django.db import models
from typing import Any
from taggit.managers import TaggableManager
from django.contrib.auth.models import*
from django.contrib.auth.models import User

# Create your models here.
class Tracking(models.Model): #models.Model เป็นการใช้ inheritance ในการสืบทอดคุณสมบัติ
    name = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    tracking = models.CharField(max_length=100,null=True,blank=True) #null,blank มักจะใช้คู่่กันกรณีที่ต้องการให้เว้นว่างข้อมูลได้
    line_id = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return '{}  {} ({})'.format(self.name,self.tel,self.tracking) 
        '''
        เมื่อมีการเรียกใช้ Tracking() จะเร่ิ่มใช้ฟังก์ชั่น str เป็นอันดับแรก โดยให้ใส่ self.name,self,tel
        และใส่หรือไม่ใส่ self.tracking
        '''

class Officer(models.Model):
    name = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    other = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return '{}  {}'.format(self.name,self.tel)    

class Ask_QA(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True,verbose_name='ชื่อผู้ติดต่อ')
    email = models.CharField(max_length=100,null=True,blank=True,verbose_name='อีเมล์')
    title = models.CharField(max_length=100,null=True,blank=True,verbose_name='หัวข้อ')
    detail = models.TextField(null=True,blank=True,verbose_name='รายละเอียด')
    detail_answer = models.TextField(null=True,blank=True,verbose_name='คำตอบ')
    
    def __str__(self):
        return '{}  ({})'.format(self.name,self.title) 

class Author(models.Model):
    author_name = models.CharField(max_length=100)     
    image = models.ImageField(upload_to='author-image/',null=True,blank=True,default='default.png')
    
    def __str__(self):
        return self.author_name
    
class Post(models.Model):
    author = models.ForeignKey(Author,on_delete = models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200,null=True,blank=True)
    body =  models.TextField(null=True,blank=True)
    images = models.ImageField(upload_to='post-image/',null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)       
    date_updated = models.DateTimeField(auto_now=True)    
    slug = models.SlugField(unique=True,max_length=180,null=True,blank=True)    
    tags = TaggableManager()
    
    def __str__(self):
        return self.title
    
class Category(models.Model):
    category_name = models.CharField(max_length=255,default='หมวดหมู่ทั่วไป')
    category_detail = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,    null=True, blank=True)
    name = models.CharField(max_length=255)
    introduction = models.TextField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    normal_price = models.IntegerField(null=True, blank=True)
    price1 = models.IntegerField(null=True, blank=True)
    price2 = models.IntegerField(null=True, blank=True)
    shipping_cost = models.IntegerField(default=40, null=True, blank=True)
    images = models.ImageField(upload_to="products/", null=True, blank=True)
    quantity = models.IntegerField(default=1)
    available = models.BooleanField(default=True)
    unit = models.CharField(max_length=255, default="-")
    image_url = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    tel = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True, blank=True)
    count = models.IntegerField(default=1)
    buyer_price = models.FloatField(default=0)
    shipping_cost = models.FloatField(default=0)
    slip = models.ImageField(upload_to="products-slip/", null=True)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    not_complete = models.BooleanField(default=False)

    
    def __str_(self):
        return self.first_name

class TrackingOrderID(models.Model):
    tracking_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_id")
    order_id = models.CharField(max_length=10)

    def __str__(self):
        return self.order_id


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    photo = models.ImageField(upload_to = 'profile_photo',null=True,blank=True)
    usertype = models.CharField(max_length=100,default='member')
    interested_in = models.CharField(max_length=100,null=True,blank=True)
    facebook = models.CharField(max_length=100,default='No Facebook')
    address = models.TextField(null=True,blank=True)
    tel = models.CharField(max_length=100,null=True,blank=True)    
    #เพิ่มใหม่
    cart_quantity = models.IntegerField(default=0,null=True,blank=True)
    
    def __str__(self):
        return self.user.username
    
class OrderProduct(models.Model):
    order_id = models.CharField(max_length=100,null=True,blank=True)
    product_id = models.CharField(max_length=100,null=True,blank=True)
    product_name = models.CharField(max_length=100,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    total = models.IntegerField(null=True,blank=True)
    
    
    def __str__(self):
        return self.product_name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100,null=True,blank=True)
    product_name = models.CharField(max_length=100,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    stamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    total = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return self.product_name
    
class CartOrder(models.Model):
    order_id = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    tel = models.CharField(max_length=14)
    email = models.CharField(max_length=50,null=True,blank=True)
    address = models.TextField()
    express = models.CharField(max_length=100)
    payment = models.CharField(max_length=100)
    other = models.TextField(null=True,blank=True)
    stamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    paid = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    slip = models.ImageField(upload_to='cart-slip/', null=True,blank=True)
    slip_time = models.DateTimeField(null=True,blank=True)
    bank_account = models.CharField(
        max_length=50,
        choices=[
            ('KBank','KBank'),
            ('SCB','SCB'),
            ('TTB','TTB'),
            ('KTB','KTB'),
            ('BAY',"BAY"),
            ('อื่น','อื่น'),
            
        ],
        default='KBank',
    )
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    tracking_number = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.order_id
    
class Discount(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    percent = models.IntegerField(default=10,null=True,blank=True)
    active = models.BooleanField(default=False)
    