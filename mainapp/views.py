from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.core.exceptions import ObjectDoesNotExist
from function import *
from mainapp.models import *
from Admin.models import *
from Staff.models import *
import pandas as pd
import os
from decoder import login_required_custom

data = load_data('Data.csv')
similarity_matrix = load_recommandation()

data.drop(['Engine Fuel Type', 'Number of Doors'], axis=1, inplace=True)
data.columns = [col.replace(" ", "_") for col in data.columns]

sample_data = data.copy()
sample_data.drop(['image_url', 'MSRP'], axis=1, inplace=True)

encoder = {}
for i in sample_data.columns:
    if sample_data[i].dtype == 'object':
        encoder[i] = load_encoder(i)

cars = data.to_dict('records')
col, row = data.shape


def recommend(matches):
    # car_index = matches.index[0]
    # similarity_scores = list(enumerate(similarity_matrix[car_index]))
    # similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    # car_indices = [i[0] for i in similarity_scores[1:9]]

    car_index = matches.index[0]
    car_indices = similarity_matrix[car_index][:8]

    available_columns = [
        col for col in [
            'Make', 'Model', 'Year', 'Engine_HP', 'Engine_Cylinders',
            'Transmission_Type', 'Driven_Wheels', 'Market_Category',
            'Vehicle_Size', 'Vehicle_Style', 'highway_MPG', 'city_mpg',
            'Popularity', 'MSRP', 'image_url'
        ]
        if col in data.columns
    ]

    return data.iloc[car_indices][available_columns]


def index(request):
    try:
        car_data = load_data('Car Data.csv')
        car_names = sorted((car_data['Make'] + ' ' + car_data['Model']).drop_duplicates(), reverse=True)

        top = {}
        for i in range(min(6, len(car_names))):
            top[f'top{i + 1}'] = car_data[
                (car_data['Make'] + ' ' + car_data['Model']) == car_names[i]
            ].iloc[0]

        context = {
            'cars': cars,
            'top': top,
        }
        return render(request, 'index.html', context)

    except Exception as e:
        return render(request, 'error.html', {'error': e})


def collection(request):
    try:
        car_data = load_data('Car Data.csv')

        filters = [
            'Make', 'Year', 'Engine_Cylinders',
            'Transmission_Type', 'Driven_Wheels',
            'Vehicle_Size', 'Vehicle_Style'
        ]

        filter_data = {}

        for filter_name in filters:
            values = car_data[filter_name].dropna().astype(str).unique().tolist()
            values = [v for v in values if v != "Not Given"]
            filter_data[filter_name] = values[:20]

        context = {
            'cars': car_data.to_dict('records'),
            'count': len(car_data),
            'filter_data': filter_data
        }

        return render(request, 'collection.html', context)

    except Exception as e:
        return render(request, 'error.html', {'error': e})


def filter(request, filter):
    try:
        car_data = load_data('Car Data.csv')

        values = list(car_data[filter].dropna().unique())

        context = {
            'tab': 'Collection',
            'filter_name': filter,
            'values': values,
            'no': len(values)
        }

        return render(request, 'filter.html', context)

    except Exception as e:
        return render(request, 'error.html', {'error': e})


def detail(request, filter, detail):
    try:
        car_data = load_data('Car Data.csv')

        cars = car_data[
            car_data[filter].astype(str).str.lower() == str(detail).lower()
        ]

        context = {
            'filter_name': filter,
            'value': detail,
            'cars': cars.to_dict('records'),
            'count': len(cars)
        }

        return render(request, 'detail.html', context)

    except Exception as e:
        return render(request, 'error.html', {'error': e})


def detail_car(request, id):
    try:
        car_data = load_data('Car Data.csv')

        car = car_data[
            car_data['Car_ID'].astype(str) == str(id)
        ]

        if car.empty:
            return render(request, 'error.html', {'error': 'Car Not Found'})

        context = {
            'car': car.iloc[0].to_dict()
        }

        return render(request, 'detail_car.html', context)

    except Exception as e:
        return render(request, 'error.html', {'error': e})


def prediction(request):
    try:
        user = request.session.get('User')
        result = None
        model = load_prediction()
        if request.method == 'POST':
            sample_dict = {
                'Make': request.POST.get('make'),
                'Model': request.POST.get('model'),
                'Year': request.POST.get('year'),
                'Engine_HP': request.POST.get('engine_hp'),
                'Engine_Cylinders': request.POST.get('engine_cylinders'),
                'Transmission_Type': request.POST.get('transmission_type'),
                'Driven_Wheels': request.POST.get('driven_wheels'),
                'Market_Category': request.POST.get('market_category'),
                'Vehicle_Size': request.POST.get('vehicle_size'),
                'Vehicle_Style': request.POST.get('vehicle_style'),
                'highway_MPG': request.POST.get('highway_mpg'),
                'city_mpg': request.POST.get('city_mpg'),
                'Popularity': request.POST.get('popularity'),
            }

            sample = pd.DataFrame([sample_dict])

            for col_name in sample.columns:
                if sample[col_name].iloc[0] in [None, '']:
                    raise ValueError(f'{col_name} is empty')

            for col_name in sample.columns:
                if col_name in encoder:
                    sample[col_name] = encoder[col_name].transform(sample[col_name])

            result = round(model.predict(sample)[0], 2)

            if user:
                PredictionHistory.objects.create(
                    Role=user['Role'],
                    Email=user['Email'],
                    Make=sample_dict['Make'],
                    Model=sample_dict['Model'],
                    Year=sample_dict['Year'],
                    Engine_HP=sample_dict['Engine_HP'],
                    Engine_Cylinders=sample_dict['Engine_Cylinders'],
                    Transmission_Type=sample_dict['Transmission_Type'],
                    Driven_Wheels=sample_dict['Driven_Wheels'],
                    Market_Category=sample_dict['Market_Category'],
                    Vehicle_Size=sample_dict['Vehicle_Size'],
                    Vehicle_Style=sample_dict['Vehicle_Style'],
                    highway_MPG=sample_dict['highway_MPG'],
                    city_mpg=sample_dict['city_mpg'],
                    Popularity=sample_dict['Popularity'],
                    MSRP=result
                )

        context = {
            'Transmission_Type': data['Transmission_Type'].dropna().drop_duplicates(),
            'Driven_Wheels': data['Driven_Wheels'].dropna().drop_duplicates(),
            'Vehicle_Size': data['Vehicle_Size'].dropna().drop_duplicates(),
            'Vehicle_Style': data['Vehicle_Style'].dropna().drop_duplicates(),
            'result': result,
        }

        return render(request, 'prediction.html', context)

    except Exception as e:
        return render(request, 'error.html', {'error': e})


def recommandation(request):
    try:
        message = ''
        cars = None
        selected_car = ''
        user = request.session.get('User')

        if request.method == 'POST':
            car_name = request.POST.get('car_name')
            car_model = request.POST.get('car_model')
            selected_car = car_name + ' ' + car_model
            matches = data[
                data["Make"].str.lower().str.contains(car_name.lower(), na=False) &
                data["Model"].str.lower().str.contains(car_model.lower(), na=False)
            ]
            if matches.empty:
                message = "Car not found in dataset."
            else:
                recommended = recommend(matches)
                cars = recommended.to_dict('records')
            if user:
                RecommandationHistory.objects.create(
                    Role=user['Role'],
                    Email=user['Email'],
                    Brand=car_name,
                    Model=car_model,
                    Data=cars
                )
        context = {
            'cars': cars,
            'message': message,
            'selected_car': selected_car
        }
        return render(request, 'recommandation.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error': e})


def about(request):
    try:
        return render(request, 'about.html', {'cars': cars})
    except Exception as e:
        return render(request, 'error.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def login(request):
    try:
        if request.method == 'POST':
            role = request.POST.get('role')
            email = request.POST.get('email')
            password = request.POST.get('password')
            if role == 'admin':
                user = Admin_Registration.objects.filter(Email=email, Password=password).first()
                if user is None:
                    return render(request, 'login.html', {'message': f'Invalid email or password for {role} {email} and {password}'})
                request.session['User'] = {
                    'Role': 'Admin',
                    'Name': user.Name,
                    'Email': user.Email,
                    'Phone_No': user.Phone_No
                }
                return redirect('Admin:Admin_Home')
            elif role == 'staff':
                user = Staff_Registration.objects.filter(Email=email, Password=password).first()
                if user is None:
                    return render(request, 'login.html', {'message': f'Invalid email or password {email} and {password}'})
                request.session['User'] = {
                    'Role': 'Staff',
                    'Name': user.Name,
                    'Email': user.Email,
                    'Phone_No': user.Phone_No
                }
                return redirect('Staff:Staff_Home')
            elif role == 'customer':
                user = Customer_Registration.objects.filter(Email=email, Password=password).first()
                if user is None:
                    return render(request, 'login.html', {'message': f'Invalid email or password {email} and {password}'})
                request.session['User'] = {
                    'Role': 'Customer',
                    'Name': user.Name,
                    'Email': user.Email,
                    'Phone_No': user.Phone_No
                }

                return redirect('mainapp:Index')

            else:
                return render(request, 'login.html', {'message': 'Invalid User Type selected'})

        return render(request, 'login.html')

    except Exception as e:
        return render(request, 'error.html', {'error': e})


def signup(request):
    try:
        if request.method == 'POST':
            role = request.POST.get('role')
            fullname = request.POST.get('fullname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            if role == 'admin':
                database = Admin_Request
                database2 = Admin_Registration
            elif role == 'staff':
                database = Staff_Request
                database2 = Staff_Registration
            elif role == 'customer':
                database = database2 = Customer_Registration
                
            else:
                return render(request, 'signup.html', {'message': 'Invalid role selected'})
            if database2.objects.filter(Email=email).exists() or database.objects.filter(Email=email).exists():
                return render(request, 'signup.html', {'message': 'Email already exists'})
            database.objects.create(Name=fullname, Email=email, Phone_No=phone, Password=password)
            return redirect('mainapp:Index')
        return render(request, 'signup.html')
    except Exception as e:
        return render(request, 'error.html', {'error': e})


def forget(request):
    try:
        if request.method == 'POST':
            role = request.POST.get('role')
            fullname = request.POST.get('fullname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            if role == 'admin':
                database = Admin_Registration
            elif role == 'staff':
                database = Staff_Registration
            elif role == 'customer':
                database = Customer_Registration
            else:
                return render(request, 'forget.html', {'message': 'Invalid role selected'})
            user = database.objects.filter(Name=fullname, Email=email, Phone_No=phone).first()
            if user is None:
                return render(request, 'forget.html', {'message': 'User not found'})
            user.Password = password
            user.save()
            return redirect('mainapp:Login')
        return render(request, 'forget.html')
    except Exception as e:
        return render(request, 'error.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def Logout(request):
    try:
        request.session.flush()
        response = redirect('mainapp:Index')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    except Exception as e:
        return render(request, 'error.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_custom
def Service(request):
    try:
        user = request.session.get('User')

        if request.method == 'POST':
            Service_Request.objects.create(
                User_Name=user['Name'],
                User_Email=user['Email'],
                Name=request.POST.get('Name'),
                Email=request.POST.get('Email'),
                Phone_No=request.POST.get('Phone_No'),
                Service_Type=request.POST.get('Service_Type'),
                Brand=request.POST.get('Brand'),
                Model=request.POST.get('Model'),
                Number=request.POST.get('Number'),
                Distance=request.POST.get('Distance'),
                Problem=request.POST.get('Problem')
            )

            return redirect('mainapp:Service')

        return render(request, 'service.html', {'user': user})

    except Exception as e:
        return render(request, 'error.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_custom
def Renting(request):
    try:
        rent_data = load_data('Rent Data.csv')
        cars = rent_data.to_dict('records')
        return render(request, 'renting.html', {'cars': cars})

    except Exception as e:
        return render(request, 'error.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_custom
def RentDetail(request, id):
    try:
        rent_data = load_data('Rent Data.csv')
        user = request.session.get('User')

        car_df = rent_data[
            rent_data['Car_ID'].astype(str) == str(id)
        ]

        if car_df.empty:
            return render(request, 'error.html', {'error': 'Car not found'})

        car = car_df.iloc[0].to_dict()
        car['Total_Amount'] = car['Rent_Price'] + car['Security']

        if request.method == 'POST':
            CarRent.objects.create(
                Car_ID=request.POST.get('Car_ID'),
                User_Name=user['Name'],
                User_Email=user['Email'],
                Name=request.POST.get('Name'),
                Email=request.POST.get('Email'),
                Phone_No=request.POST.get('Phone_No'),
                Pickup_Date=request.POST.get('Pickup_Date'),
                Return_Date=request.POST.get('Return_Date'),
                Address=request.POST.get('Address')
            )

            rent_data.loc[
                rent_data['Car_ID'].astype(str) == str(id),
                'Status'
            ] = 'Booked'

            save_data(rent_data, 'Rent Data.csv')

            return redirect('mainapp:Renting')

        return render(request, 'rentingdetail.html', {'car': car})

    except Exception as e:
        return render(request, 'error.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_custom
def BuyNow(request, id):
    try:
        car_data = load_data('Car Data.csv')
        user = request.session.get('User')

        car_df = car_data[
            car_data['Car_ID'].astype(str) == str(id)
        ]

        if car_df.empty:
            return render(request, 'error.html', {'error': 'Car not found'})

        car = car_df.iloc[0].to_dict()

        if request.method == 'POST':
            CarOrder.objects.create(
                Car_ID=request.POST.get('Car_ID'),
                User_Name=user['Name'],
                User_Email=user['Email'],
                Name=request.POST.get('Name'),
                Email=request.POST.get('Email'),
                Phone_No=request.POST.get('Phone_No'),
                Address=request.POST.get('Address'),
                Payment_Mode=request.POST.get('Payment_Mode'),
                Delivery_Type='Home Delivery',
                Status='Pending',
                Message=f"Order placed for {car['Make']} {car['Model']}"
            )

            return redirect('mainapp:History')

        return render(request, 'buynow.html', {'car': car})

    except Exception as e:
        return render(request, 'error.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_custom
def History(request):
    try:
        car_data = load_data('Car Data.csv')
        rent_data = load_data('Rent Data.csv')
        selling_data = load_data('Selling Data.csv')
        sold_data = load_data('Sold Data.csv')
        sold_selling_data = load_data('Sold Selling Data.csv')

        user = request.session.get('User')

        orders = CarOrder.objects.filter(
            User_Email=user['Email']
        ).order_by('-Order_ID')

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

            order_list.append({'order': order, 'car': car})

        sold_cars = CarSelling.objects.filter(
            User_Email=user['Email']
        ).order_by('-Sell_ID')

        sold_list = []

        for order in sold_cars:
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

            sold_list.append({'order': order, 'car': car})

        rent_cars = CarRent.objects.filter(
            User_Email=user['Email']
        ).order_by('-Rent_ID')

        rent_list = []

        for order in rent_cars:
            car = None

            car_df = rent_data[
                rent_data['Car_ID'].astype(str) == str(order.Car_ID)
            ]

            if not car_df.empty:
                car = car_df.iloc[0].to_dict()

            rent_list.append({'order': order, 'car': car})

        prediction_history = PredictionHistory.objects.filter(
            Role=user['Role'],
            Email=user['Email']
        ).order_by('-Predict_ID')

        recommendation_history = RecommandationHistory.objects.filter(
            Role=user['Role'],
            Email=user['Email']
        ).order_by('-Recommandation_ID')

        context = {
            'orders': order_list,
            'sold_cars': sold_list,
            'rent_orders': rent_list,
            'prediction_history': prediction_history,
            'recommendation_history': recommendation_history,
        }

        return render(request, 'history.html', context)

    except Exception as e:
        return render(request, 'error.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_custom
def OrderDetail(request, type, id):
    try:
        car_data = load_data('Car Data.csv')
        rent_data = load_data('Rent Data.csv')
        selling_data = load_data('Selling Data.csv')
        sold_data = load_data('Sold Data.csv')
        sold_selling_data = load_data('Sold Selling Data.csv')

        user = request.session.get('User')
        order_list = []

        if type == 'Order':
            orders = CarOrder.objects.filter(
                User_Email=user['Email'],
                Order_ID=id
            ).first()

            if orders is None:
                return render(request, 'error.html', {'error': 'Order not found'})

            if orders.Status in ['Pending', 'Approved', 'Rejected']:
                select_data = car_data
            elif orders.Status == 'Delivered':
                select_data = sold_data
            else:
                return render(request, 'error.html', {'error': 'Order not found'})

        elif type == 'Sold':
            orders = CarSelling.objects.filter(
                User_Email=user['Email'],
                Sell_ID=id
            ).first()

            if orders is None:
                return render(request, 'error.html', {'error': 'Selling order not found'})

            if orders.Status in ['Pending', 'Approved', 'Rejected']:
                select_data = selling_data
            elif orders.Status == 'Delivered':
                select_data = sold_selling_data
            else:
                return render(request, 'error.html', {'error': 'Selling order not found'})

        elif type == 'Rent':
            orders = CarRent.objects.filter(
                User_Email=user['Email'],
                Rent_ID=id
            ).first()

            if orders is None:
                return render(request, 'error.html', {'error': 'Rent order not found'})

            select_data = rent_data

        else:
            return render(request, 'error.html', {'error': 'Invalid history type'})

        car_df = select_data[
            select_data['Car_ID'].astype(str) == str(orders.Car_ID)
        ]

        if car_df.empty:
            return render(request, 'error.html', {'error': 'Car data not found'})

        car = car_df.iloc[0].to_dict()

        order_list.append({
            'order': orders,
            'car': car,
            'type': type,
            'Status': orders.Status
        })

        context = {
            'order_list': order_list
        }

        return render(request, 'order_detail.html', context)

    except Exception as e:
        return render(request, 'error.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_custom
def Selling(request):
    try:
        selling_data = load_data('Selling Data.csv')
        user = request.session.get('User')

        if request.method == 'POST':
            if len(selling_data) == 0:
                car_id = 1
            else:
                car_id = int(selling_data['Car_ID'].max()) + 1

            sample = pd.DataFrame([{
                'Car_ID': car_id,
                'Make': request.POST.get('Make'),
                'Model': request.POST.get('Model'),
                'Year': request.POST.get('Year'),
                'Engine_HP': request.POST.get('Engine_HP'),
                'Engine_Cylinders': request.POST.get('Engine_Cylinders'),
                'Transmission_Type': request.POST.get('Transmission_Type'),
                'Driven_Wheels': request.POST.get('Driven_Wheels'),
                'Market_Category': request.POST.get('Market_Category'),
                'Vehicle_Size': request.POST.get('Vehicle_Size'),
                'Vehicle_Style': request.POST.get('Vehicle_Style'),
                'highway_MPG': request.POST.get('highway_MPG'),
                'city_mpg': request.POST.get('city_mpg'),
                'Popularity': request.POST.get('Popularity'),
                'MSRP': request.POST.get('MSRP'),
                'image_url': request.POST.get('image_url')
            }])

            if selling_data.empty:
                selling_data = sample.copy()
            else:
                selling_data = pd.concat([selling_data, sample], ignore_index=True)

            save_data(selling_data, 'Selling Data.csv')

            CarSelling.objects.create(
                Car_ID=car_id,
                User_Name=user['Name'],
                User_Email=user['Email'],
                Name=request.POST.get('Name'),
                Email=request.POST.get('Email'),
                Phone_No=request.POST.get('Phone_No')
            )

            return redirect('mainapp:Selling')

        return render(request, 'selling.html')

    except Exception as e:
        return render(request, 'error.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_custom
def RecommandationDetail(request, id):
    try:
        user = request.session.get('User')

        recommendation = RecommandationHistory.objects.filter(
            Recommandation_ID=id,
            Role=user['Role'],
            Email=user['Email']
        ).first()

        if recommendation is None:
            return render(request, 'error.html', {'error': 'Recommandation not found'})

        context = {
            'recommendation': recommendation
        }

        return render(request, 'recommandationdetail.html', context)

    except Exception as e:
        return render(request, 'error.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_custom
def PredictionDetail(request, id):
    try:
        user = request.session.get('User')

        prediction = PredictionHistory.objects.filter(
            Predict_ID=id,
            Role=user['Role'],
            Email=user['Email']
        ).first()

        if prediction is None:
            return render(request, 'error.html', {'error': 'Prediction not found'})

        context = {
            'prediction': prediction
        }

        return render(request, 'predictiondetail.html', context)

    except Exception as e:
        return render(request, 'error.html', {'error': e})


def error(request):
    return render(request, 'error.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_custom
def customerprofile(request):
    try:
        context = {
            'user': request.session.get('User')
        }
        return render(request, 'customerprofile.html', context)

    except Exception as e:
        return render(request, 'error.html', {'error': e})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
@login_required_custom
def notication(request):
    try:
        user = request.session.get('User')

        context = {
            'user': user,
            'notifications': NotificationModel.objects.filter(Role__in=['Customer', 'All'])
        }

        return render(request, 'customernotication.html', context)

    except Exception as e:
        return render(request, 'error.html', {'error': e})