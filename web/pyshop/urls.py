from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home ,name='home'),
    path('cart/',views.cart ,name='cart'),
    path('update_add/<slug>',views.update_add ,name='update_add'),
    path('update_remove/<slug>',views.update_remove ,name='update_remove'),
    path('product/<slug>',views.product ,name='product'),
    path('add_to_cart/<slug>',views.add_to_cart ,name='add'),
    path('remove_from_cart/<slug>',views.remove_from_cart ,name='remove'),
    path('checkout/',views.checkout ,name='checkout'),
    path('shirt/',views.shirt ,name='shirt'),
    path('sportswear/',views.sportswear ,name='sportswear'),
    path('outwear/',views.outwear ,name='outwear'),
    path('signup',views.signup ,name='signup'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('login/',auth_views.LoginView.as_view(),name='login')
]