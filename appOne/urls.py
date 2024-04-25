from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from appOne import views
from .models import Equipment
from appOne.forms import EquipmentFilterForm


urlpatterns = [

# created by Saad
    path('', views.welcomePage, name="welcomepage"),
    path('homePage/', views.homePage, name="homepage"),
    path("contact-us/", views.contactUsPage, name="contact_us"),
    path('equipment-list/', views.equipmentList, name='equipment_list'),
    path('equipment/add/', views.equipment_add, name='equipment_add'),

    path('equipment/<int:equipment_id>/edit/', views.equipment_edit, name='equipment_edit'),
    path('equipment/<int:equipment_id>/delete/', views.equipment_delete, name='equipment_delete'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/<int:pk>/reserve/', views.equipment_reserve, name='equipment_reserve'),

    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('cart/place-booking/', views.place_booking, name='place_booking'),
    path('cart/place-booking/', views.equipment_reserve, name='place_booking'),

    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='welcomepage'), name='logout'),
    path('user/orders/', views.user_orders, name='user_orders'),
    path('cancel-reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),


    #johan
    path('admin_home/', views.admin_home, name='admin_home'),
    path('user_home/', views.user_home, name='user_home'),
    path('management/', views.management_view, name='management'),
    path('manage-booking/', views.manage_booking_view, name='manage_booking'),
    path('reports/', views.reports_view, name='reports'),
    path('about/', views.about_view, name='about'),
    
]
