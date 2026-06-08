from django.shortcuts import render, redirect
from Admin.models import *
from mainapp.models import *
from function import *
import os
from decoder import admin_required
from django.views.decorators.cache import cache_control


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def AdminHome(request):
    try:
        sold_data = load_data('Sold Data.csv')
        sold_selling_data = load_data('Sold Selling Data.csv')
        user = request.session.get('User')

        context = {
            'user': user,
            'total_admin_request': Admin_Request.objects.count(),
            'total_staff_request': Staff_Request.objects.count(),
            'total_customers': Customer_Registration.objects.count(),
            'total_notifications': NotificationModel.objects.count(),
            'total_admins': Admin_Registration.objects.count(),
            'total_staff': Staff_Registration.objects.count(),
            'total_service_request': Service_History.objects.count(),
            'total_rent_request': CarRent.objects.filter(Status='Pending').count(),
            'total_buy_request': CarOrder.objects.filter(Status='Pending').count(),
            'total_selling_request': CarSelling.objects.filter(Status='Pending').count(),
            'total_buy_history': len(sold_data),
            'total_selling_history': len(sold_selling_data),
        }

        return render(request, 'adminindex.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def Logout(request):
    try:
        request.session.flush()
        response = redirect('mainapp:Index')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def AdminRequest(request):
    try:
        user = request.session.get('User')
        context = {
            'user': user,
            'requests': Admin_Request.objects.all()
        }
        return render(request, 'adminrequest.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def StaffRequest(request):
    try:
        user = request.session.get('User')
        context = {
            'user': user,
            'requests': Staff_Request.objects.all()
        }
        return render(request, 'staffrequest.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def AdminManagement(request):
    try:
        user = request.session.get('User')
        context = {
            'user': user,
            'users': Admin_Registration.objects.all()
        }
        return render(request, 'adminmanagement.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def StaffManagement(request):
    try:
        user = request.session.get('User')
        context = {
            'user': user,
            'users': Staff_Registration.objects.all()
        }
        return render(request, 'staffmanagement.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def CustomerManagement(request):
    try:
        user = request.session.get('User')
        context = {
            'user': user,
            'users': Customer_Registration.objects.all()
        }
        return render(request, 'customermanagement.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def ServicRequest(request):
    try:
        user = request.session.get('User')
        context = {
            'user': user,
            'requests': Service_Request.objects.filter(Status='Pending')
        }
        return render(request, 'servicrequest.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def RentRequest(request):
    try:
        rent_data = load_data('Rent Data.csv')
        user = request.session.get('User')
        orders = CarRent.objects.filter(Status='Pending')

        order_list = []

        for order in orders:
            car = None
            car_df = rent_data[
                rent_data['Car_ID'].astype(str) == str(order.Car_ID)
            ]

            if not car_df.empty:
                car = car_df.iloc[0].to_dict()

            order_list.append({
                'order': order,
                'car': car
            })

        context = {
            'user': user,
            'requests': order_list
        }

        return render(request, 'rentrequest.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def BuyRequest(request):
    try:
        car_data = load_data('Car Data.csv')
        user = request.session.get('User')
        orders = CarOrder.objects.filter(Status='Pending')

        order_list = []

        for order in orders:
            car = None
            car_df = car_data[
                car_data['Car_ID'].astype(str) == str(order.Car_ID)
            ]

            if not car_df.empty:
                car = car_df.iloc[0].to_dict()

            order_list.append({
                'order': order,
                'car': car
            })

        context = {
            'user': user,
            'requests': order_list
        }

        return render(request, 'buyrequest.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def SellingRequest(request):
    try:
        selling_data = load_data('Selling Data.csv')
        user = request.session.get('User')
        orders = CarSelling.objects.filter(Status='Pending')

        order_list = []

        for order in orders:
            car = None
            car_df = selling_data[
                selling_data['Car_ID'].astype(str) == str(order.Car_ID)
            ]

            if not car_df.empty:
                car = car_df.iloc[0].to_dict()

            order_list.append({
                'order': order,
                'car': car
            })

        context = {
            'user': user,
            'requests': order_list
        }

        return render(request, 'sellingrequest.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def ServicHistory(request):
    try:
        user = request.session.get('User')
        context = {
            'user': user,
            'services': Service_History.objects.all().order_by('-Service_ID')
        }
        return render(request, 'adminservice.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def RentHistory(request):
    try:
        rent_data = load_data('Rent Data.csv')
        user = request.session.get('User')
        orders = CarRent.objects.all().order_by('-Rent_ID')

        order_list = []

        for order in orders:
            car = None
            car_df = rent_data[
                rent_data['Car_ID'].astype(str) == str(order.Car_ID)
            ]

            if not car_df.empty:
                car = car_df.iloc[0].to_dict()

            order_list.append({
                'order': order,
                'car': car
            })

        context = {
            'user': user,
            'rents': order_list
        }

        return render(request, 'adminrent.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def BuyHistory(request):
    try:
        car_data = load_data('Car Data.csv')
        sold_data = load_data('Sold Data.csv')
        user = request.session.get('User')
        orders = CarOrder.objects.all().order_by('-Order_ID')

        order_list = []

        for order in orders:
            car = None

            if order.Status in ['Pending', 'Approved', 'Rejected']:
                select_data = car_data
            elif order.Status == 'Delivered':
                select_data = sold_data
            else:
                continue

            car_df = select_data[
                select_data['Car_ID'].astype(str) == str(order.Car_ID)
            ]

            if not car_df.empty:
                car = car_df.iloc[0].to_dict()

            order_list.append({
                'order': order,
                'car': car
            })

        context = {
            'user': user,
            'history': order_list
        }

        return render(request, 'adminbuy.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def SellingHistory(request):
    try:
        selling_data = load_data('Selling Data.csv')
        sold_selling_data = load_data('Sold Selling Data.csv')
        user = request.session.get('User')
        orders = CarSelling.objects.all().order_by('-Sell_ID')

        order_list = []

        for order in orders:
            car = None

            if order.Status in ['Pending', 'Approved', 'Rejected']:
                select_data = selling_data
            elif order.Status == 'Delivered':
                select_data = sold_selling_data
            else:
                continue

            car_df = select_data[
                select_data['Car_ID'].astype(str) == str(order.Car_ID)
            ]

            if not car_df.empty:
                car = car_df.iloc[0].to_dict()

            order_list.append({
                'order': order,
                'car': car
            })

        context = {
            'user': user,
            'history': order_list
        }

        return render(request, 'adminselling.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def Notification(request):
    try:
        if request.method == 'POST':
            role = request.POST.get('role')
            title = request.POST.get('title')
            message = request.POST.get('message')

            NotificationModel.objects.create(
                Role=role,
                Title=title,
                Message=message
            )

        user = request.session.get('User')

        context = {
            'user': user,
            'notifications': NotificationModel.objects.all().order_by('-Date')
        }

        return render(request, 'notification.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def Profile(request):
    try:
        user = request.session.get('User')
        context = {
            'user': user
        }
        return render(request, 'adminprofile.html', context)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def error(request):
    return render(request, 'adminerror.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def ApproveAdminRequest(request, role, email):
    try:
        if role == 'Admin':
            database_request = Admin_Request
            database_registration = Admin_Registration
            redirect_url = 'Admin:Admin_Request'

        elif role == 'Staff':
            database_request = Staff_Request
            database_registration = Staff_Registration
            redirect_url = 'Admin:Staff_Request'

        else:
            return render(request, 'adminerror.html', {'error': 'Invalid role'})

        user = database_request.objects.filter(Email=email).first()

        if user:
            if not database_registration.objects.filter(Email=user.Email).exists():
                database_registration.objects.create(
                    Name=user.Name,
                    Email=user.Email,
                    Phone_No=user.Phone_No,
                    Password=user.Password
                )

            user.delete()

        return redirect(redirect_url)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def RemoveAdminRequest(request, role, email):
    try:
        if role == 'Admin':
            database_request = Admin_Request
            redirect_url = 'Admin:Admin_Request'

        elif role == 'Staff':
            database_request = Staff_Request
            redirect_url = 'Admin:Staff_Request'

        else:
            return render(request, 'adminerror.html', {'error': 'Invalid role'})

        user = database_request.objects.filter(Email=email).first()

        if user:
            user.delete()

        return redirect(redirect_url)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def RemoveUser(request, role, email):
    try:
        if role == 'Admin':
            database = Admin_Registration
            redirect_url = 'Admin:Admin_Management'

        elif role == 'Staff':
            database = Staff_Registration
            redirect_url = 'Admin:Staff_Management'

        elif role == 'Customer':
            database = Customer_Registration
            redirect_url = 'Admin:Customer_Management'

        else:
            return render(request, 'adminerror.html', {'error': 'Invalid role'})

        user = database.objects.filter(Email=email).first()

        if user:
            user.delete()

        return redirect(redirect_url)

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def ApproveServiceRequest(request, id):
    try:
        service = Service_Request.objects.filter(Service_ID=id).first()

        if service:
            service.Status = 'Approved'
            service.save()

        return redirect('Admin:Service_Request')

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def RejectServiceRequest(request, id):
    try:
        service = Service_Request.objects.filter(Service_ID=id).first()

        if service:
            service.Status = 'Rejected'
            service.save()

        return redirect('Admin:Service_Request')

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def ApproveRentRequest(request, id):
    try:
        rent_data = load_data('Rent Data.csv')
        service = CarRent.objects.filter(Rent_ID=id).first()

        if service:
            rent_data.loc[
                rent_data['Car_ID'].astype(str) == str(service.Car_ID),
                'Status'
            ] = 'Not Available'

            save_data(rent_data, 'Rent Data.csv')

            service.Status = 'Approved'
            service.save()

        return redirect('Admin:Rent_Request')

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def RemoveRentRequest(request, id):
    try:
        service = CarRent.objects.filter(Rent_ID=id).first()

        if service:
            service.Status = 'Rejected'
            service.save()

        return redirect('Admin:Rent_Request')

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def ApproveBuyRequest(request, id):
    try:
        service = CarOrder.objects.filter(Order_ID=id).first()

        if service:
            service.Status = 'Approved'
            service.save()

        return redirect('Admin:Buy_Request')

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def RemoveBuyRequest(request, id):
    try:
        service = CarOrder.objects.filter(Order_ID=id).first()

        if service:
            service.Status = 'Rejected'
            service.save()

        return redirect('Admin:Buy_Request')

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def ApproveSellingRequest(request, id):
    try:
        service = CarSelling.objects.filter(Sell_ID=id).first()

        if service:
            service.Status = 'Approved'
            service.save()

        return redirect('Admin:Selling_Request')

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@admin_required
def RemoveSellingRequest(request, id):
    try:
        service = CarSelling.objects.filter(Sell_ID=id).first()

        if service:
            service.Status = 'Rejected'
            service.save()

        return redirect('Admin:Selling_Request')

    except Exception as e:
        return render(request, 'adminerror.html', {'error': e})