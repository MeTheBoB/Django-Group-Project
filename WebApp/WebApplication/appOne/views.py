from django.shortcuts import render
from django.http import HttpResponse
from .models import*
# Create your views here.




def welcomePage(request):
    return render(request, "appOne/welcomePage.html")


def index(request):
    return HttpResponse(request, {'testdata':testdata})

def homePage(request,id):
    listitem = Item.objects.get(id=id)
    context = {'listitem':listitem}
    return render(request, "appOne/home.html", context)

#
# def homePage(request):
#     my_dict = {"insert_me": "Hello this is my first insertion"}
#     return render(request, "appOne/home.html", context=my_dict)


def contactUsPage(request):
    item = Item.objects.all
    context = {"item":item}
    return render(request, "appOne/contactus.html",context)
