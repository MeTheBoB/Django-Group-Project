from django.urls import path
from appOne import views


urlpatterns = [
    path("",views.welcomePage),
    path('homePage/',views.homePage),
    path("contact-us/",views.contactUsPage,name="contact_us"),


]
