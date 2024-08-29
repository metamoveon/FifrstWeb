from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required #ไลบราลีสำหรับบังคับ login required
from myapp.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.core.files.storage import FileSystemStorage
import string
import random


# Create your views here.
# Models Template Views (MTV.) เป็นโมเดลสำหรับ Django

def Home(request):
    return render(request,'myapp/home.html')

def About_us(request):
    return render(request,'myapp/about-us.html')

def Contact(request):
    return render(request,'myapp/contact.html')

def TrackingPage(request):
    tracks = Tracking.objects.all() #methoc objects.all() เป็นคำสั่งพิเศษที่ดึงข้อมูลทั้งหมดใน Tracking
    context = {'tracks':tracks}
    return render(request,'myapp/tracking.html',context)

def Ask(request):
    if request.method == 'POST':
        data = request.POST.copy()
        #print('DATA :',data)
        name = data.get('name')
        email = data.get('email')
        title = data.get('title')
        detail = data.get('detail')
        print(name,email,title,detail)
        
        new = Ask_QA()
        new.name = name
        new.email = email
        new.title = title
        new.detail = detail
        new.save()
        
    return render(request,'myapp/ask.html')

@login_required #คำสั่งบังคับให้ลอกอินทุกครั้งก่อนที่จะเข้าไปดูที่ Question ในเวป
def Question(request):
    question = Ask_QA.objects.all() #method objects.all() เป็นคำสั่งพิเศษที่ดึงข้อมูลทั้งหมดใน Tracking
    context = {'question':question}
    return render(request,'myapp/question.html',context)

@login_required
def Answer(request,askid):
    #localhost:8000/answer/askid
    
    record = Ask_QA.objects.get(id=askid)
    
    if request.method == 'POST':
        data = request.POST.copy()
        #askid = data.get('askid')
        detail_answer = data.get('detail_answer')
        record.detail_answer = detail_answer
        record.save()
        
    context = {'record':record}
        
    return render(request,'myapp/answer.html',context)


def Sawatdee(request):
    return HttpResponse('<h1>สวัสดีจ้า<h1>')

    
def Posts(request):
    posts = Post.objects.all().order_by('id').reverse()[:3]

    context = {"posts": posts}

    return render(request, 'myapp/blog.html',context)


def PostDetail(request, slug):
    posts = Post.objects.all().order_by('id').reverse()[:3]
    try:
        single_post = get_object_or_404(Post, slug=slug)
        print("รายละเอียดบทความ", single_post)
    except Post.DoesNotExist:
        return render(request, 'myapp/home.html')
    
    context = {"single_post": single_post, "posts": posts}
    
    return render(request, 'myapp/blog-detail.html', context)

def Register(request):
    
    context = {}
    
    if request.method == 'POST':
        data = request.POST.copy()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        check = User.objects.filter(username=email)
        if len(check) == 0:
            newuser = User()
            newuser.username = email
            newuser.first_name = name
            newuser.set_password(password)
            newuser.save()
            
            profile = Profile()
            profile.user = newuser
            profile.save()
            
            context['success'] = 'success'
        else:
            context['usertaken'] = 'usertaken'
        
        
    return render(request,'myapp/register.html',context)

def Login(request):
    
    context = {}
    
    if request.method == 'POST':
        data = request.POST.copy()
        email = data.get('email')
        password = data.get('password')
        
        check = User.objects.filter(username=email)
        if len(check) == 0:
            context['nouser'] = 'nouser'
        else:
            try:
                user = authenticate(username=email,password=password)
                login(request,user)
                print('Login Completed')
                return redirect('question')
            except:
                context['wrongpassword'] = 'wrongpassword'
           
        
        
    return render(request,'myapp/login.html',context)

def AllProduct(request):
    all_product = Product.objects.filter(available=True)
    
    context={'all_Product':all_product}
    return render(request,'myapp/all-product.html',context )
      
def RandomOrderID():
    ro_id = ""
    ro_id += random.choice(string.ascii_uppercase)
    ro_id += random.choice(string.ascii_uppercase)

    for i in range(8):
        ro_id += random.choice("0123456789")
    
    return ro_id


def ProductDetail(request, slug):
    RandomOrderID()
    product = Product.objects.get(slug=slug)
    context = {"product": product, "product_price": product.normal_price}

    if product.price1 > 0:
        price_1 = (product.price1 * 100) / product.normal_price

        context["price_1"] = 100 - int(price_1)
        context["product_price"] = product.price1
    if product.price2 > 0:
        price_2 = (product.price2 * 100) / product.normal_price

        context["price_2"] = 100 - int(price_2)

    if request.method == "POST":
        data = request.POST.copy()

        new_order = Order()
        # new_order.user = product
        new_order.products = product
        new_order.first_name = data.get("first_name")
        new_order.last_name = data.get("last_name")
        new_order.tel = data.get("tel")
        new_order.email = data.get("email")
        new_order.address = data.get("address")
        new_order.count = data.get("count")
        new_order.buyer_price = data.get("buyer_price")
        new_order.shipping_cost = data.get("shipping_cost")
        
        try:
            file_image = request.FILES["upload_slip"]
            file_image_name = request.FILES["upload_slip"].name.replace(" ", "")
            file_system_storage = FileSystemStorage()
            file_name = file_system_storage.save(
                "products-slip/" + file_image_name, file_image
            )
            upload_file_url = file_system_storage.url(file_name)
            new_order.slip = upload_file_url[6:]
        except:
            new_order.slip = "/default.png"

        new_order.save()
        # เพิ่ม function random id 
        try:
            tracking_id = TrackingOrderID.objects.all()
            while True:
                order_ID = RandomOrderID()
                for tid in tracking_id:
                    if order_ID == tid.order_id:
                        continue
                break
        except:
            order_ID = RandomOrderID()

        new_tracking_id = TrackingOrderID()
        new_tracking_id.tracking_order =  new_order
        new_tracking_id.order_id = order_ID
        new_tracking_id.save()
        
        return redirect('tracking-ordr-id-page',order_ID)

    return render(request, "myapp/product-detail.html", context)

def TrackingOrderId(request, tid):
    tracking_id = TrackingOrderID.objects.get(order_id=tid).tracking_order
    buyer_price = tracking_id.buyer_price

    if buyer_price == int(buyer_price):
        buyer_price = int(buyer_price)

    shipping_cost = tracking_id.shipping_cost
    if shipping_cost == int(shipping_cost):
        shipping_cost = int(shipping_cost)

    all_price = tracking_id.buyer_price + tracking_id.shipping_cost

    context = {
        "tracking_id": tracking_id,
        "buyer_price": buyer_price,
        "order_id":tid,
        "shipping_cost":shipping_cost,
        "all_price":all_price
    }

    return render(request, "myapp/tracking-order.html", context)


def DiscountPage(request):
    
    if request.user.discount.active == True:
        return redirect('all-product')
    
    context = {}
    
    if request.method == 'POST':
        data = request.POST.copy()
        check = data.get('discount')
        print('CHECK',check)
        
        if check == 'check-true':
            # request.user.discount.active = True
            user = User.objects.get(username = request.user.username)
            discount = Discount.objects.get(user=user)
            discount.active = True
            discount.save()
            
            return redirect('all-product')
        
    return render(request,'myapp/discount.html',context)

def AddToCart(request, pid):
    username = request.user.username
    user = User.objects.get(username=username)
    check = Product.objects.get(id=pid)


    try:
        new_cart = Cart.objects.get(user=user, product_id=str(pid))
        new_quantity = new_cart.quantity + 1
        new_cart.quantity = new_quantity
        calculate = new_cart.price * new_quantity
        new_cart.total = calculate
        new_cart.save()


        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])


        updated_quantity = Profile.objects.get(user=user)
        updated_quantity.cart_quantity = count
        updated_quantity.save()


        return redirect('all-product')
   
    except:
        new_cart = Cart()
        new_cart.user = user
        new_cart.product_id = pid
        new_cart.product_name = check.name
        new_cart.price = int(check.normal_price)
        new_cart.quantity = 1
        calculate = int(check.normal_price) * 1
        new_cart.total = calculate
        new_cart.save()


        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updated_quantity = Profile.objects.get(user=user)
        updated_quantity.cart_quantity = count
        updated_quantity.save()


        return redirect('all-product')


def MyCart(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}
    
    if request.method == 'POST':
        data = request.POST.copy()
        product_id = data.get('product_id')
    
        try:
            item = Cart.objects.get(user=user,product_id = product_id)
            item.delete()
            context['status'] = 'delete'
        except Cart.DoesNotExist:
            item = None
        
        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updated_quantity = Profile.objects.get(user=user)
        updated_quantity.cart_quantity = count
        updated_quantity.save()
        
    mycart = Cart.objects.filter(user=user)
    count = sum([c.quantity for c in mycart])
    total = sum([c.total for c in mycart])
    
    context['mycart'] = mycart
    context['count'] = count
    context['total'] = total
    
    return render(request,'myapp/my-cart.html',context)

def MyCartEdit(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}
    
    if request.method == 'POST':
        data = request.POST.copy()
        
        print('I have data',data)
        if data.get("clear") == "clear":
            Cart.objects.filter(user=user).delete()
            updated_quantity = Profile.objects.get(user=user)
            updated_quantity.cart_quantity = 0
            updated_quantity.save()
            return redirect("my-cart")
        
        edit_list = []
        for k,v in data.items():
            if k[:2] == 'pd':
                pid = int(k.split("_")[1])
                dt = [pid, int(v)]
                edit_list.append(dt)
        
        for ed in edit_list:
            edit_cart = Cart.objects.get(product_id=ed[0],user=user)
            edit_cart.quantity = ed[1]
            calculate = edit_cart.price * ed[1]
            edit_cart.total = calculate
            edit_cart.save()
            
        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updated_quantity = Profile.objects.get(user=user)
        updated_quantity.cart_quantity = count
        updated_quantity.save()
        
        return redirect('my-cart')
    
    mycart = Cart.objects.filter(user=user)
    context["mycart"] = mycart
    return render(request,'myapp/my-cart-edit.html',context)
            
            
        
            



    
        


