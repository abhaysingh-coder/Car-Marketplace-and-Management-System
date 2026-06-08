from Staff import views
from django.urls import path
app_name='Staff'

urlpatterns = [
   path('', views.StaffHome, name = 'Staff_Home'),
   path('Service/', views.ServicRequest, name = 'Service'),
   path('Renting/', views.RentRequest, name = 'Renting'),
   path('Buying/', views.BuyRequest, name = 'Buying'),
   path('Selling/', views.SellingRequest, name = 'Selling'),
   path('Notification/', views.Notification, name = 'Notification'),
   path('Profile/', views.Profile, name = 'Profile'),
   path('Error',views.error, name='Error'),
   path('Logout',views.Logout, name='Logout'),
   path('Complete_Buy/<int:id>',views.CompleteBuy, name='Complete_Buy'),
   path('Complete_Rent/<int:id>',views.CompleteRent, name='Complete_Rent'),
   path('Complete_Service/<int:id>',views.CompleteService, name='Complete_Service'),
   path('Complete_Selling/<int:id>',views.Completeselling, name='Complete_Selling'),
]