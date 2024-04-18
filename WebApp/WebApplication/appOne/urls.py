from django.urls import path
from appOne import views
from .models import Equipment
from appOne.forms import EquipmentFilterForm


urlpatterns = [
    path("",views.welcomePage,name="welcomepage"),
    path('homePage/',views.homePage, name="homepage"),
    path("contact-us/",views.contactUsPage,name="contact_us"),
    path('equipment-list/', views.equipmentList, name='equipment_list'),
    path('equipment/add/', views.equipment_add, name='equipment_add'),
    path('equipment/<int:equipment_id>/edit/', views.equipment_edit, name='equipment_edit'),
    path('equipment/add/', views.equipment_add, name='equipment_add'),
    path('equipment/edit/<int:equipment_id>/', views.equipment_edit, name='equipment_edit'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('admin-login/', views.admin_login, name='adminLogin'),
    # path('logout/', views.logout_view, name='logout'),
    # path('welcome/', views.welcome_view, name='welcome'),


]
