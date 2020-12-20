from django.urls import path
from . import views as home_views
from product import views as product_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home_views.HomeView.as_view(), name="home"),
    path('products/', product_views.allProductView,
         name="products"),
     path('products/gth/<str:category>/', product_views.allProductView,
         name="category-product"),
     path('filter_products/', product_views.filterProductView,
         name="filter_products"),
    path('products/<int:pk>/', product_views.ProductDetailView,
         name="product-detail"),
    path('products/<int:pk>/stock/',
         product_views.instockview, name="presentinstock"),
    path('profile/bag/', product_views.BagView, name="bagview"),

    path('applyCoupon', product_views.applyCouponView, name="applyCoupon"),
    
    path('bag/placeorder/', product_views.PlaceOrderView, name="place-order"),
    path('bag/placeorder/createorder',
         product_views.CreateOrderView, name="create-order"),
    #placeorder
    path('create-address/ajax/',product_views.createAddressAjax,name="create-address-ajax"),
    path('handle/paytm/',product_views.handlePaytmResponse,name="handle-paytm-response"),

    #localBag
    path('get-product-detail/<int:pk>',product_views.getProductDetail,name="get-product-detail"),

    #addtowishlist
    path('addWishlist/<int:pro_id>',product_views.AddToWishlist,name="add_to_wishlist"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
