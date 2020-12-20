from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse,HttpResponse , HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.template.defaulttags import register

from django.views.generic import (
    ListView,
    DetailView,
    CreateView
)
from django.views import View
from .models import (
    Product,
    Category,
    ProductDetail,
    BagItem,
    Order,
    OrderItem,
    Wishlists,
    Coupon
)
from users.models import Address
from django.core import serializers
import json
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import ProductSerializer,ProductDetailSerializer
from rest_framework.renderers import JSONRenderer
from PayTm import Checksum
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def allProductView(request,category = None):
    if request.method == 'GET':
        print(category)

        search = request.GET.get("search",None)
        print(search)
        context = {}
       
        if category is not None:
            context[category] = True
            category_id = get_object_or_404(Category,name = category).id 
            products = Product.objects.filter(category = category_id)
        else:
            products = Product.objects.all()

        if search != None:
            products = products.filter(Q(category__name__icontains = search) | Q(name__icontains = search) | Q(description__icontains = search))
        
        paginator = Paginator(products,10)
        try:
            page = paginator.page(1)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            print("empty")
            page = paginator.page(paginator.num_pages)


        prod = []

        
        for product in page:
            current = {}
            current["id"] = product.id 
            current["name"] = product.name 
            current["price"] = product.price 
            
            color_temp = []
            color = []

            size = []
            variations = product.variations.all()
            for variation in variations:
                if variation.color not in color_temp:
                    color_temp.append(variation.color)
                    color.append(variation.color)
                if variation.size not in size:
                    size.append(variation.size)

            current["sizes"] = size 
            current["colors"] = color
            current["image"] = product.variations.first().image1.url 

            prod.append(current)

        print(prod)

        context['products'] = prod
        context['page_obj'] = page
        if search is not None:
            context['search_value'] = search
        return render(request,'product/categorywiseproduct-list.html',context)


price_dict = {
    'small':{
        'min':239,
        'max':499
    },
    'mid':{
        'min':499,
        'max':999
    },
    'high':{
        'min':999,
        'max':1499
    }
}
def filterProductView(request):
    if request.method == 'GET' and request.is_ajax:
        category = request.GET.get("category", None)
        price = request.GET.get("price",None)
        color = request.GET.get("color",None)
        size = request.GET.get("size",None)
        sort_order = request.GET.get("sort",None)
        search = request.GET.get("query",None)
        page_no = request.GET.get("page",None)

    

        price = json.loads(price)
        category = json.loads(category)
        color = json.loads(color)
        size = json.loads(size)
        page_no = int(page_no)
       
        products = Product.objects.all()

        if search != None:
            products = Product.objects.filter(Q(category__name__icontains = search) | Q(name__icontains = search) | Q(description__icontains = search))
        
        query = None
        first = False
        for i in category:
            if first == False and category[i] != 'None':
                query = Q(category__name = category[i])
                first = True
            elif category[i] != 'None':
                query |= Q(category__name = category[i])
        if query is not None:
            products = products.filter(query)

        first = False

        query = None
        for i in price:
            if first == False and price[i] != 'None':
                query = Q(price__range = (price_dict[price[i]]['min'],price_dict[price[i]]['max']))
                first = True
            elif price[i] != 'None':
                query |= Q(price__range = (price_dict[price[i]]['min'],price_dict[price[i]]['max']))

        if query is not None:
            products = products.filter(query)

        first = False

        query = None
        for i in color:
            if first == False and color[i] != 'None':
                query = Q(variations__color = color[i])
                first = True
            elif color[i] != 'None':
                query |=  Q(variations__color = color[i])

        if query is not None:
            products = products.filter(query).distinct()

        first = False

        query = None
        for i in size:
            if first == False and size[i] != 'None':
                query = Q(variations__size = size[i])
                first = True
            elif size[i] != 'None':
                query |=  Q(variations__size = size[i])

        if query is not None:
            products = products.filter(query).distinct()


        if sort_order == 'random':
            pass
        elif sort_order == 'new':
            pass
        elif sort_order == 'incr':
            products = products.order_by('price')
        elif sort_order == 'decr':
            products = products.order_by('-price')

    
        #Pagination       
        paginator = Paginator(products,10)
        try:
            page = paginator.page(page_no)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            print("empty")
            page = paginator.page(paginator.num_pages)
             
       
        serializer = ProductSerializer(page,many = True)

        #getting the page obj attributes in page_dict as page objects are not serializable
        page_dict = {}
        page_dict['has_other_pages'] = page.has_other_pages()
        page_dict['has_next'] = page.has_next()
        page_dict['has_previous'] = page.has_previous()
        if page.has_previous():
            page_dict['previous_page_number'] = page.previous_page_number()
        if page.has_next():
            page_dict['next_page_number'] = page.next_page_number()

        page_dict['has_previous'] = page.has_previous()
        page_dict['num_pages'] = page.paginator.num_pages
        page_dict['number'] = page.number  
        page_json = json.dumps(page_dict)
              
        return JsonResponse({"valid":True,"products":serializer.data,"page_obj":page_json},status=200)
    return JsonResponse({},status=400)

"""
def allProductView(request):

    productDetails = ProductDetail.objects.all()
    products = Product.objects.all()
    mydict = dict()
    @register.filter
    def from_dict(d, k):
        return d[k]
    for productDetail in productDetails:
        mydict[productDetail.product.id] = {
                'color': [],
                'size' : [],
        } 
    for productDetail in productDetails:
        if productDetail.color not in mydict[productDetail.product.id]['color']:
            mydict[productDetail.product.id]['color'].append(productDetail.color)
        if productDetail.size not in mydict[productDetail.product.id]['size']:
            mydict[productDetail.product.id]['size'].append(productDetail.size)

    paginator = Paginator(productDetails,9)
    page = request.GET.get('page')
    productDetails = paginator.get_page(page)
    
    for productDetail in productDetails:
        for items in mydict[productDetail.product.id]:       
            print(items) 
            # for size in items['size']:
            #     print(size) 
    
    context = {
        'productDetails': productDetails,
        'mydict': mydict,
    
    }
    return render(request,'product/categorywiseproduct-list.html',context)
"""

def ProductDetailView(request,pk):
    product = Product.objects.get(id = pk)
    variations = ProductDetail.objects.all().filter(product__id = pk)
    size = {
    "S":"Small",
    "M":"Medium",
    "L":"Large",
    "XL":"XLarge"
    }
    size_temp = dict()
    print(type(size_temp))
    for variation in variations:
        if variation.size not in size_temp:
            size_temp[variation.size] = size[variation.size]
    
    color = []
    variation_list = []
    for variation in variations:
        if variation.color not in color:
            color.append(variation.color)
            variation_list.append(variation)

    context = {
        'variations':variation_list,
        'recommended':Product.objects.all()[:10],
        'product':product,
        'size':size_temp
    }
    return render(request,'product/product-detail2.html',context)
    




def instockview(request, pk):
    if request.method == 'GET' and request.is_ajax:
        size = request.GET.get("size", None)
        color = request.GET.get("color", None)
        if ProductDetail.objects.filter(product=pk, size=size, color=color,quantity__gte=1).exists():
            return JsonResponse({"valid": True}, status=200)
        else:
            return JsonResponse({"valid": False}, status=200)
    return JsonResponse({}, status=400)

def getProductDetail(request,**kwargs):
    if request.method == 'GET':
        size = request.GET.get("size", None)
        color = request.GET.get("color", None)
        product = Product.objects.filter(id=kwargs['pk']).first()
        if ProductDetail.objects.filter(product=product, color=color, size=size,quantity__gte=1).exists():
            product_detail_object = ProductDetail.objects.filter(
                product=product, color=color, size=size).first()
            serializer = ProductDetailSerializer(product_detail_object)

            product_info = {}
            product_info["name"] = product.name
            product_info["category"] = product.category.name
            product_info["description"] = product.description
            product_info["price"] = product.price
            product_info["discount_price"] = product.discount_price

            product_info_json = json.dumps(product_info)
            return JsonResponse({"valid":True,"product_detail":serializer.data,"product_info":product_info_json},status=200)
        return JsonResponse({"valid": False}, status=200)
    return JsonResponse({}, status=400)

def BagView(request):
    return render(request,'product/bag.html')

def PlaceOrderView(request):
    if request.user.is_authenticated:
        return render(request, "product/placeorder.html")
    else:
        return redirect("account-registration")

@login_required
def createAddressAjax(request):
    if request.method == 'POST' and request.is_ajax:
        name = request.POST.get('name')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        postcode = request.POST.get('postcode')
        city = request.POST.get('city')
        phone = request.POST.get('phone')

        address = Address(name = name,address1 = address1,address2 = address2, postcode = postcode, city = city,phone = phone)
        address.save()
        address.users.add(request.user)
        address_dict = {}
        address_dict['address1'] = address1
        address_dict['address2'] = address2
        address_dict['name'] = name
        address_dict['phone'] = phone
        address_dict['city'] = city 
        address_dict['postcode'] = postcode 
        address_dict['address_id'] = address.id 
        address_json = json.dumps(address_dict) 
        return JsonResponse({"valid":True,"address":address_json},status=200)
    return JsonResponse({},status=400)


def applyCouponView(request):
    print(request.GET.get('coupon'))
    if request.method == 'GET':

        coupon = request.GET.get('coupon')
        orderTotal = int(request.GET.get('amount'))
        print("yes")
        if Coupon.objects.filter(pattern = coupon).exists():
            print("yass")
            couponItem = Coupon.objects.filter(pattern = coupon).first()
            if couponItem.min_total_required <= orderTotal:
                if couponItem.is_percentage:
                    discount = ((couponItem.amount)*orderTotal)/100
                else:
                    discount = couponItem.amount
                return JsonResponse({"valid":True,"discount":discount},status=200)

    return JsonResponse({"valid":False},status=200)


MERCHANT_KEY = 'ZPKM#upRee1&0ml4'

@csrf_exempt
def handlePaytmResponse(request):   
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
    return render(request, 'product/paymentstatus.html', {'response': response_dict})



shippingCharges = {
        '110025':'25',
        '110063':'30'
}

@login_required
def CreateOrderView(request):
    if request.method == 'POST':
        address_id = request.POST['address_id']
        bag_details = request.POST['bag']
        bag_details = json.loads(bag_details)
        coupon = request.POST['coupon']
        


        total = 0
        for item in bag_details:
            product_detail_id = bag_details[item]["id"]
            product_detail_object =  ProductDetail.objects.get(id=product_detail_id)
            price = product_detail_object.product.discount_price 
            quantity = int(bag_details[item]["wanted_quantity"])
            total += price*quantity
            print(product_detail_id)

        print(total)

        #subtracting the coupons discount
        if Coupon.objects.filter(pattern = coupon).exists():
            print("yass")
            couponItem = Coupon.objects.filter(pattern = coupon).first()
            if couponItem.min_total_required <= total:
                if couponItem.is_percentage:
                    discount = ((couponItem.amount)*total)/100
                else:
                    discount = couponItem.amount

                total = total - discount 


        #adding the shipping charges

        
        address = Address.objects.get(id=address_id)
        pincode = address.postcode

        if pincode in shippingCharges:
          deliveryCharge = int(shippingCharges[pincode])
          total = total + deliveryCharge
         
        order = Order(user=request.user, address=address, amount = total)
        order.save()

        for item in bag_details:
            product_detail_id = bag_details[item]["id"]
            product_detail_object =  ProductDetail.objects.get(id=product_detail_id)
            quantity = bag_details[item]["wanted_quantity"]
            OrderItem.objects.create(
                order=order, product_detail=product_detail_object, quantity=quantity)

        
        messages.success(request, f'Your Order has been made!')

        print(order.id)
        param_dict = {

                'MID': 'UNuigS14231700215219',
                'ORDER_ID': str(order.id),
                'TXN_AMOUNT': str(total),
                'CUST_ID': str(request.user.id),
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handle/paytm/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'product/paytm.html', {'param_dict': param_dict})

class ListOrdersView(LoginRequiredMixin,ListView):
    template_name = "users/orders.html"
    context_object_name = "orderItems"
    
    def get_queryset(self):
        mydict = []
        orders = Order.objects.filter(user=self.request.user)
        
        for order in orders:
            orderItem = OrderItem.objects.filter(order=order)
            for ordering in orderItem:
                mydict.append(ordering)
 
        return mydict
   

class ListOrderItemsView(LoginRequiredMixin,ListView):
    template_name = "users/order-itemslist.html"
    context_object_name = "items"
    
    #for adding two number inside HTML
    @register.filter
    def add(total, gst):
        return total+gst

    def get_queryset(self):

        return OrderItem.objects.filter(order=self.kwargs['pk'])


        
        mydict = {}
        mylist = []
        total = 0
        orderItems = OrderItem.objects.filter(order=self.kwargs['pk'])
        users = User.objects.get(username=self.request.user)
        mydict['email'] = users.email
        mydict['user'] = users.username

        for orderItem in orderItems:
            mydict['date'] = orderItem.order.created
            mydict['id'] = orderItem.order.id
            mydict['address'] = orderItem.order.address.address1
            mydict['phone'] = orderItem.order.address.phone
            mydict['city'] = orderItem.order.address.city
            mydict['pincode'] = orderItem.order.address.postcode
            total = total + orderItem.quantity * orderItem.order.amount
        mydict['total'] = total
        mylist.append(mydict)
        mylist.append(orderItems)
        print(mylist)
        return mylist




@login_required
def AddToWishlist(request,pro_id):

    curr_user = request.user


    wishlist = Wishlists.objects.get_or_create(user = curr_user ,
                products =Product.objects.get(id=pro_id)

                )

    

        
    messages.success(request, f'Added to Wishlist')



    return redirect('product-detail' , pro_id)
    # st = "Item Added" + str(wishlist.products.name)
    # return HttpResponse(wishlist)
