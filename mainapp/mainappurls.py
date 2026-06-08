from mainapp import views
from django.contrib import admin
from django.urls import path
app_name='mainapp'

urlpatterns = [
   path('', views.index, name='Index'),
   path('Collection/', views.collection, name='Collection'),
   path('Collection/<str:filter>/', views.filter, name='Filter'),
   path('Collection/<str:filter>/<str:detail>/', views.detail, name='Detail'),
   path('Collection/<int:id>', views.detail_car, name='Detail_Car'),
   path('Prediction/', views.prediction, name='Prediction'),
   path('Recommandation/', views.recommandation, name='Recommandation'),
   path('About/', views.about, name='About'),
   path('Login/', views.login, name='Login'),
   path('Forget/', views.forget, name='Forget'),
   path('Sign_UP/', views.signup, name='Sign_UP'), 
   path('Error', views.error, name='Error'),
   path('Logout', views.Logout, name='Logout'),
   path('Service/', views.Service, name = 'Service'),
   path('Renting', views.Renting, name = 'Renting'),
   path('Selling', views.Selling, name = 'Selling'),
   path('Renting/<int:id>', views.RentDetail, name = 'Rent_Detail'),
   path('History', views.History, name='History'),
   path('History/Prediction/<int:id>', views.PredictionDetail, name = 'Prediction_Detail'),
   path('History/Recommendation/<int:id>', views.RecommandationDetail, name = 'Recommendation_Detail'),
   path('History/<str:type>/<int:id>', views.OrderDetail, name = 'Order_Detail'),
   path('Buy_Now/<int:id>', views.BuyNow, name='Buy_Now'),
   path('Profile', views.customerprofile, name='CustomerProfile'),
   path('Notification', views.notication, name='Notification'),
]