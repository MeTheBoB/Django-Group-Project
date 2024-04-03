from django.urls import path
from appOne import views


urlpatterns = [
    path("",views.welcomePage,name="welcomepage"),
    path('homePage/<str:id>',views.homePage, name="homepage"),
    path("contact-us/",views.contactUsPage,name="contact_us"),



]
