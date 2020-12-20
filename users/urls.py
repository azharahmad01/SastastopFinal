from django.urls import path,include
from . import views as user_views
from product import views as product_views
import django.contrib.auth.views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # wishlist
    path('wishlist', user_views.wishlist_view, name='wishlist_view'),

    # user authentication
    path('', user_views.register, name='account-registration'),
    path('logout/', user_views.logOutUser, name='logout'),
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html'
            ),
        name='password_reset'),
    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
            ),
        name='password_reset_done'),   
    path('password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'),
    name='password_reset_confirm'),
    path('password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
    name='password_reset_complete'),
    path('password-change/',
    auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html'),
    name='password_change'),
    path('password_change/done/',
    auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'),
    name='password_change_done'),



   #address
   path('profile/',user_views.ProfileView.as_view(),name="profile"),
   path('profile-Details/',user_views.ProfileDetails,name="profile-details"),
   path('profile-Edit/',user_views.ProfileEdit,name="profile-edit"),
   path('profile/addresses',user_views.AddressView,name="addresses"),
   path('profile/addresses/create',user_views.createAddressView,name="create-address"),
   path('profile/addresses/delete/<int:pk>/',user_views.deleteAddressView,name="delete-address"),
   path('profile/addresses/update/<int:pk>/',user_views.getUpdateFormView,name="get-update-form"),
   path('profile/addresses/update/<int:pk>/done/',user_views.UpdateAddressFormView,name="update-address"),
   path('profile/orders',product_views.ListOrdersView.as_view(),name="orders"),
   path('profile/orders/<int:pk>/items',product_views.ListOrderItemsView.as_view(),name="order-items"),


]


if settings.DEBUG:
	 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
