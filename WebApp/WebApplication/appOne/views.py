from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import*
from .forms import EquipmentFilterForm
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .forms import*
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm


def welcomePage(request):
    return render(request, "appOne/welcomePage.html")


def index(request):
    return HttpResponse(request, {'testdata':testdata})

def homePage(request):
    return render(request, "appOne/home.html")

def contactUsPage(request):
    return render(request, "appOne/contactus.html")


def equipmentList(request):
    filter_form = EquipmentFilterForm(request.GET or None)
    equipments = Equipment.objects.all()

    if filter_form.is_valid():
        equipment_id = filter_form.cleaned_data.get('equipment_id')
        type_of_device = filter_form.cleaned_data.get('type_of_device')

        if equipment_id:
            equipments = equipments.filter(equipment_id=equipment_id)

        if type_of_device:
            equipments = equipments.filter(type_of_device__icontains=type_of_device)

    context = {
        'equipments': equipments,
        'filter_form': filter_form,
    }

    return render(request, 'appOne/equipmentList.html', context)


def equipment_add(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = EquipmentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('equipment_list')
        else:
            form = EquipmentForm()
        return render(request, 'appOne/equipment_form.html', {'form': form})
    else:
        return HttpResponseForbidden()


def equipment_edit(request, equipment_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    equipment = get_object_or_404(Equipment, pk=equipment_id)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm(instance=equipment)

    return render(request, 'appOne/equipment_form.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('welcomePage')
    else:
        form = SignUpForm()
    return render(request, 'appOne/user/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('welcomepage')
    else:
        form = AuthenticationForm()
    return render(request, 'appOne/user/login.html', {'form': form})


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and (user.is_staff or user.is_superuser):
            login(request, user)
            return redirect('welcomepage')
    return render(request, 'appOne/user/adminLogin.html')
