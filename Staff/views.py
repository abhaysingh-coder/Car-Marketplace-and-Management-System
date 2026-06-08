from django.shortcuts import render, redirect
from Admin.models import *
from mainapp.models import *
from function import *
from decoder import staff_required
from django.views.decorators.cache import cache_control


global car_data
global rent_data
global selling_data
global sold_data
global sold_selling_data

car_data = load_data('Car Data.csv')
rent_data = load_data('Rent Data.csv')
selling_data = load_data('Selling Data.csv')
sold_data = load_data('Sold Data.csv')
sold_selling_data = load_data('Sold Selling Data.csv')

# Create your views here.

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@staff_required
def StaffHome(request):
    try:
        user = request.session.get('User')
        context ={
            'user': user,
            'total_service_request': Service_Request.objects.filter(Status='Approved').count(),
            'total_rent_request': CarRent.objects.filter(Status='Approved').count(),
            'total_buy_request': CarOrder.objects.filter(Status='Approved').count(),
            'total_selling_request': CarSelling.objects.filter(Status='Approved').count(),
        }
        return render(request, 'staffindex.html', context)
    except Exception as e:
        return render(request, 'stafferror.html', {'error':e})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@staff_required
def ServicRequest(request):
    try:
        user = request.session.get('User')
        context ={
            'user': user,
            'services' : Service_Request.objects.filter(Status='Approved'),
            'service_history': Service_History.objects.all(),
        }
        return render(request, 'staffservice.html', context)
    except Exception as e:
        return render(request, 'stafferror.html', {'error':e})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@staff_required
def RentRequest(request):
    try:
        user = request.session.get('User')
        orders = CarRent.objects.filter(Status='Approved')
        order_request = []
        for order in orders:
            car = None
            car_df = rent_data[rent_data['Car_ID'].astype(str) == str(order.Car_ID)]
            if not car_df.empty:
                car = car_df.iloc[0].to_dict()
            order_request.append({'order': order,'car': car})
        orders = CarRent.objects.filter(Status__in=['Approved', 'Delivered'])
        order_history = []
        for order in orders:
            car = None
            car_df = rent_data[rent_data['Car_ID'].astype(str) == str(order.Car_ID)]
            if not car_df.empty:
                car = car_df.iloc[0].to_dict()
            order_history.append({'order': order,'car': car})
        context ={
            'user': user,
            'rent_requests': order_request,
            'rent_history': order_history,
        }
        return render(request, 'staffrent.html', context)
    except Exception as e:
        return render(request, 'stafferror.html', {'error':e})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@staff_required
def BuyRequest(request):
    try:
        user = request.session.get('User')
        orders = CarOrder.objects.filter(Status='Approved')
        order_request = []
        for order in orders:
            car = None
            car_df = rent_data[rent_data['Car_ID'].astype(str) == str(order.Car_ID)]
            if not car_df.empty:
                car = car_df.iloc[0].to_dict()
            order_request.append({'order': order,'car': car})
        orders = CarOrder.objects.filter(Status__in=['Approved', 'Delivered'])
        order_history = []
        for order in orders:
            car = None
            if order.Status == 'Approved':
                select = car_data
            elif order.Status == 'Delivered':
                select = sold_data
            else:
                pass
            car_df = select[select['Car_ID'].astype(str) == str(order.Car_ID)]
            if not car_df.empty:
                car = car_df.iloc[0].to_dict()
            order_history.append({'order': order,'car': car})
        context ={
            'user': user,
            'buy_requests': order_request,
            'buy_history': order_history,
        }
        return render(request, 'staffbuying.html', context)
    except Exception as e:
        return render(request, 'stafferror.html', {'error':e})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@staff_required
def SellingRequest(request):
    try:
        user = request.session.get('User')
        orders = CarSelling.objects.filter(Status='Approved')
        order_request = []
        for order in orders:
            car = None
            car_df = rent_data[rent_data['Car_ID'].astype(str) == str(order.Car_ID)]
            if not car_df.empty:
                car = car_df.iloc[0].to_dict()
            order_request.append({'order': order,'car': car})
        orders = CarSelling.objects.filter(Status__in=['Approved', 'Delivered'])
        order_history = []
        for order in orders:
            car = None
            if order.Status == 'Approved':
                select = selling_data
            elif order.Status == 'Delivered':
                select = sold_selling_data
            else:
                pass
            car_df = select[select['Car_ID'].astype(str) == str(order.Car_ID)]
            if not car_df.empty:
                car = car_df.iloc[0].to_dict()
            order_history.append({'order': order,'car': car})
        context ={
            'user': user,
            'selling_requests': order_request,
            'selling_history': order_history,
        }
        return render(request, 'staffselling.html', context)
    except Exception as e:
        return render(request, 'stafferror.html', {'error':e})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@staff_required
def Notification(request):
    try:
        user = request.session.get('User')
        context ={
            'user': user,
            'notifications':NotificationModel.objects.filter(Role__in=['Staff', 'All'])
        }
        return render(request, 'staffnotification.html', context)
    except Exception as e:
        return render(request, 'stafferror.html', {'error':e})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@staff_required
def Profile(request):
    try:
        user = request.session.get('User')
        activities.objects.create(Role= user.get('Role'), Email=user.get('Email'), Activity='Staff Profile Accessed')
        context ={
            'user': user,
            'user': request.session.get('User')
        }
        return render(request, 'staffprofile.html', context)
    except Exception as e:
        return render(request, 'stafferror.html', {'error':e})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@staff_required
def error(request):
    return render(request, 'stafferror.html')

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@staff_required
def Logout(request):
    try:
        request.session.flush()
        response = redirect('mainapp:Index')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    except Exception as e:
        return render(request, 'stafferror.html', {'error': e})
    
@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@staff_required
def CompleteBuy(request, id):
    try:
        global car_data, sold_data
        service = CarOrder.objects.filter(Order_ID =id).first()
        if service:
            sample = car_data[car_data['Car_ID'] == service.Car_ID]
            sold_data = pd.concat([sold_data, sample], ignore_index=True)
            car_data = car_data.drop(sample.index)
            sold_data.to_csv('../Data/Sold Data.csv', index=False)
            car_data.to_csv('../Data/Car Data.csv', index=False)
            service.Status = 'Delivered'
            service.save()
        return redirect('Staff:Buying')
    except Exception as e:
        return render(request, 'stafferror.html', {'error': e})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@staff_required
def CompleteService(request, id):
    try:
        service = Service_Request.objects.filter(Service_ID=id).first()
        if service:
            Service_History.objects.create(Service_ID = service.Service_ID, Name = service.Name, Email = service.Email, Phone_No = service.Phone_No, Service_Type = service.Service_Type, Brand = service.Brand, Model = service.Model, Number = service.Number, Distance = service.Distance, Problem = service.Problem)
            service.delete()
        return redirect('Staff:Service')
    except Exception as e:
        return render(request, 'stafferror.html', {'error': e})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@staff_required
def CompleteRent(request, id):
    try:
        service = CarRent.objects.filter(Rent_ID=id).first()
        if service:
            rent_data.loc[rent_data['Car_ID'] == service.Car_ID, 'Status'] = 'Available'
            service.Status = 'Delivered'
            rent_data.to_csv('../Data/Rent Data.csv', index=False)
            service.save()
        return redirect('Staff:Renting')
    except Exception as e:
        return render(request, 'stafferror.html', {'error': e})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@staff_required
def Completeselling(request, id):
    try:
        global selling_data, sold_selling_data
        service = CarSelling.objects.filter(Sell_ID =id).first()
        if service:
            sample = selling_data[selling_data['Car_ID'] == service.Car_ID]
            sold_selling_data = pd.concat([sold_selling_data, sample], ignore_index=True)
            selling_data = selling_data.drop(sample.index)
            sold_selling_data.to_csv('../Data/Sold Selling Data.csv', index=False)
            selling_data.to_csv('../Data/Selling Data.csv', index=False)
            service.Status = 'Delivered'
            service.save()
        return redirect('Staff:Selling')
    except Exception as e:
        return render(request, 'stafferror.html', {'error': e})
