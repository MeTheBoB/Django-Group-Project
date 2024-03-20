from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.



testdata = [
{"id":1, "name":"item 1 of the list"},
{"id":2, "name":"item 2 of the list"},
{"id":3, "name":"item 3 of the list"},


]


def welcomePage(request):
    return render(request, "appOne/welcomePage.html")


def index(request):
    return HttpResponse("Hello World! this is home")


def homePage(request):
    my_dict = {"insert_me": "Hello this is my first insertion"}
    return render(request, "appOne/home.html", context=my_dict)


def contactUsPage(request):
    return render(request, "appOne/contactus.html")
