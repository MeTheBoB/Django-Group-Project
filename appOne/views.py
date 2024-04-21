from django.shortcuts import render
from django.http import HttpResponse
from .models import*
from .forms import EquipmentFilterForm
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .forms import*
from django.contrib.auth.decorators import login_required


@login_required
def equipmentList(request):
    # ... existing logic ...
    is_admin = request.user.is_staff
    context = {
        'equipments': equipments,
        'is_admin': is_admin,  # Add this line to pass to the template
        # ... any other context data ...
    }
    return render(request, 'appOne/equipmentList.html', context)

def reports_view(request):
    # Your view logic here
    return render(request, 'appOne/reports.html')

def manage_booking_view(request):
    # Your view logic here
    return render(request, 'appOne/manage_booking.html')

def help_view(request):
    # Your logic for the help view
    return render(request, 'appOne/help.html')

def contact_us_view(request):
    # Your logic for the contact us view
    return render(request, 'appOne/contact_us.html')

def contact_view(request):
    # Logic for contact page goes here if needed
    return render(request, 'contact.html', {})

def homePage(request):
    # Your code to handle the request
    return render(request, 'appOne/home.html', context)


def management_view(request):
    # Your logic here
    return render(request, 'appOne/management.html')

def about_view(request):
    # Your about page logic
    return render(request, 'about.html')

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

    is_admin = request.user.is_staff
    context = {
        'equipments': equipments,
        'filter_form': filter_form,
        'is_admin': is_admin,  
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


def user_login(request):
    # Add your user login logic here.
    # If the user is already logged in, redirect them to their dashboard, otherwise to the login page
    if request.user.is_authenticated:
        return redirect('user_home')
    else:
        # If it's a POST request, you would handle the login form submission here
        if request.method == 'POST':
            # Perform form validation, authentication, etc.
            pass
        return render(request, 'user_login.html', {})

def admin_login(request):
    # Similar logic for admin login
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_home')
    else:
        # If it's a POST request, handle the login form submission here
        if request.method == 'POST':
            # Perform form validation, authentication, etc.
            pass
        return render(request, 'admin_login.html', {})