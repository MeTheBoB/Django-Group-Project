from django.urls import path
from appOne import views
from .models import Equipment
from appOne.forms import EquipmentFilterForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.welcomePage,name="welcomepage"),
    path('homePage/',views.homePage, name="homepage"),
    path("contact-us/",views.contactUsPage,name="contact_us"),
    path('equipment-list/', views.equipmentList, name='equipment_list'),
    path('equipment/add/', views.equipment_add, name='equipment_add'),
    path('equipment/<int:equipment_id>/edit/', views.equipment_edit, name='equipment_edit'),
     path('equipment/add/', views.equipment_add, name='equipment_add'),
    path('equipment/edit/<int:equipment_id>/', views.equipment_edit, name='equipment_edit'),
     path('', views.homePage, name='home'),
    path('management/', views.management_view, name='management'),
    path('about/', views.about_view, name='about'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('management/', views.management_view, name='management'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('equipment/add/', views.equipment_add, name='equipment_add'),
    path('reports/', views.reports_view, name='reports'),
    path('manage-booking/', views.manage_booking_view, name='manage_booking'),
    path('help/', views.help_view, name='help'),
    path('contact-us/', views.contact_us_view, name='contact_us'),
    path('contact/', views.contact_view, name='contact'),
    path('user_login/', views.user_login, name='user_login'),
    path('admin_login/', views.admin_login, name='admin_login'),


]
