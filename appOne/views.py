from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from .models import*
from .forms import EquipmentFilterForm
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError
from .forms import*
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now

# Function to check if as user is an admin
def admin_check(user):
    return user.is_authenticated and user.is_staff
# Function to check if a user is not authenticated
def is_not_authenticated(user):
    return not user.is_authenticated

# View to render the welcome page for unauthenticated users
@user_passes_test(is_not_authenticated, login_url='homepage', redirect_field_name=None)
def welcomePage(request):
    return render(request, "appOne/welcomePage.html")



# View to render the homepage for logged-in users
@login_required
def homePage(request):
    return render(request, "appOne/home.html")

# View to render the contact page for logged-in users
@login_required
def contactUsPage(request):
    return render(request, "appOne/contactus.html")


#Equipment handling
# View to display a list of equipment, with filtering options
# Created by saad and html by Johan
@login_required
def equipmentList(request):
    form = EquipmentFilterForm(request.GET or None)
    if form.is_valid():
        equipment_id = form.cleaned_data.get('equipment_id')
        type_of_device = form.cleaned_data.get('type_of_device')
        equipments = Equipment.objects.all()
        if equipment_id:
            equipments = equipments.filter(id=equipment_id)
        if type_of_device:
            equipments = equipments.filter(type_of_device__icontains=type_of_device)
    else:
        equipments = Equipment.objects.all()

    return render(request, 'appOne/equipmentList.html', {
        'filter_form': form,
        'equipments': equipments
    })


#Created by saad
# View to add new equipment to the list (for admins only)
@user_passes_test(admin_check)
def equipment_add(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)
        if form.is_valid():
            equipment = form.save()
            return redirect('equipment_list')
        else:
            print(form.errors)
    else:
        form = EquipmentForm()

    return render(request, 'appOne/equipment_form.html', {'form': form, 'equipment': None})

#Created by saad
# View to edit existing equipment (for admins only)
@user_passes_test(admin_check)
def equipment_edit(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'appOne/equipment_form.html', {'form': form, 'equipment': equipment})

#Created by saad
# View to delete equipment (for admins only)
@user_passes_test(admin_check)
def equipment_delete(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    equipment.delete()
    messages.success(request, "Equipment successfully deleted!")
    return redirect('equipment_list')


#Created by saad sharo did html
# View to display details of a specific piece of equipment
@login_required
def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    reservation_form = ReservationForm(request.POST or None)

    if request.method == 'POST':
        if 'add_to_cart' in request.POST:
            cart = request.session.get('cart', {})
            reservation_details = {
                'booking_start_date': request.POST['booking_start_date'],
                'booking_end_date': request.POST['booking_end_date'],
                'purpose': request.POST['purpose'],
                'user': request.user.id
            }
            cart[str(equipment.id)] = reservation_details
            request.session['cart'] = cart
            messages.success(request, "Item added to cart.")
            return redirect('equipment_list')
        elif reservation_form.is_valid():
            pass

    return render(request, 'appOne/equipment_detail.html', {
        'equipment': equipment,
        'form': reservation_form
    })


#User Registering and login views
#Created by saad
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'user/register.html', {'form': form})





#Cart handlings
#Created by saad
@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    for pk, reservation_details in cart.items():
        try:
            equipment = Equipment.objects.get(pk=pk)
            user = User.objects.get(pk=reservation_details['user'])
            cart_items.append({
                'equipment': equipment,
                'start_date': reservation_details['booking_start_date'],
                'end_date': reservation_details['booking_end_date'],
                'purpose': reservation_details['purpose'],
                'user': user.get_username()
            })
        except Equipment.DoesNotExist:
            messages.error(request, f'An item in your cart could not be found.')
            continue
        except User.DoesNotExist:
            messages.error(request, f'User information for an item in your cart could not be found.')
            continue
    return render(request, 'appOne/cart.html', {'cart_items': cart_items})


#Created by saad
def add_to_cart(request, pk):
    if request.method == 'POST':
        try:
            equipment = Equipment.objects.get(pk=pk)
            booking_start_date = request.POST.get('booking_start_date')
            booking_end_date = request.POST.get('booking_end_date')
            purpose = request.POST.get('purpose')

            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                equipment=equipment,
                defaults={
                    'booking_start_date': booking_start_date,
                    'booking_end_date': booking_end_date,
                    'purpose': purpose
                }
            )
            if not created:
                cart_item.booking_start_date = booking_start_date
                cart_item.booking_end_date = booking_end_date
                cart_item.purpose = purpose
                cart_item.save()

            messages.success(request, f'Added {equipment.device_name} to your cart.')
            return redirect('equipment_list')
        except Equipment.DoesNotExist:
            messages.error(request, 'This item does not exist.')
            return redirect('equipment_list')

#Created by saad
def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})

    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Item not in cart.")

    return redirect('view_cart')

#Created by saad
@login_required
def update_cart_item(request, pk):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        start_date = request.POST.get('booking_start_date')
        end_date = request.POST.get('booking_start_date')
        purpose = request.POST.get('purpose')

        if pk in cart:
            cart[pk] = {'quantity': 1, 'start_date': start_date, 'end_date': end_date, 'purpose': purpose}
            request.session['cart'] = cart
            messages.success(request, "Cart updated successfully.")
        else:
            messages.error(request, "Item not in cart.")

        return redirect('view_cart')


#equipment booking handling
#Created by saad
@login_required
def equipment_reserve(request, pk):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.equipment = equipment
            reservation.save()
            messages.success(request, "Reservation successfully created.")
            return redirect('equipment_list')
        else:
            return render(request, 'appOne/equipment_detail.html', {'form': form, 'equipment': equipment})
    else:
        form = ReservationForm()
        return render(request, 'appOne/equipment_detail.html', {'equipment': equipment, 'form': form})


#Created by saad
@login_required
def place_booking(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            messages.error(request, "No items in your cart.")
            return redirect('view_cart')

        for cart_item in cart_items:
            try:
                Reservation.objects.create(
                    equipment=cart_item.equipment,
                    user=request.user,
                    booking_start_date=cart_item.booking_start_date,
                    booking_end_date=cart_item.booking_start_date,
                    purpose=cart_item.purpose,
                )
            except Exception as e:
                messages.error(request, f"Failed to create reservation: {str(e)}")
                return redirect('view_cart')

        cart_items.delete()
        messages.success(request, "All bookings placed successfully.")
        return redirect('equipment_list')
    return redirect('view_cart')




#user order management (user) handling
#Created by saad
@login_required
def user_orders(request):
    user_reservations = Reservation.objects.filter(user=request.user)
    for reservation in user_reservations:
        reservation.is_overdue = timezone.now() >= reservation.booking_end_date
        if not reservation.is_overdue:
            reservation.days_left = (reservation.booking_end_date - timezone.now()).days
        else:
            reservation.days_left = -1

    context = {
        'reservations': user_reservations
    }
    return render(request, 'user/user_orders.html', context)
#Created by saad
@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if not reservation.is_overdue and (reservation.status != 'approved' or not reservation.status):
        reservation.delete()
        messages.success(request, "Reservation cancelled successfully.")
    else:
        messages.error(request, "You cannot cancel this reservation as it is either approved or overdue.")

    return redirect('user_orders')

#Show all users to admin
#created by Leandro
@user_passes_test(admin_check)
def list_users(request):
    users = User.objects.all()
    return render(request, 'appOne/user_list.html', {'users': users})

#Admin funtion to edit user's details
#created by Leandro
@user_passes_test(admin_check)
def add_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'New user {user.username} added successfully!')
            return redirect('list_users')
    else:
        form = SignUpForm()
    return render(request, 'user/add_user.html', {'form': form})

#Admin funtion to delete a user
#created by Leandro
@user_passes_test(admin_check)
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('list_users')


#Admin funtion to approve new bookings
#created by Leandro
@user_passes_test(admin_check)
def authorize_reservations(request):
    pending_reservations = Reservation.objects.filter(status='pending')
    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        reservation.status = 'approved'
        reservation.save()
        messages.success(request, "Reservation approved successfully.")
        return redirect('authorize_reservations')
    return render(request, 'appOne/authorize_reservations.html', {'reservations': pending_reservations})

