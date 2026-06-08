from Admin import views
from django.contrib import admin
from django.urls import path
app_name='Admin'

urlpatterns = [
   path('', views.AdminHome, name = 'Admin_Home'),
   path('Logout/', views.Logout, name = 'Logout'),
   path('Admin_Request/', views.AdminRequest, name = 'Admin_Request'),
   path('Staff_Request/', views.StaffRequest, name = 'Staff_Request'),
   path('Admin_Management/', views.AdminManagement, name = 'Admin_Management'),
   path('Staff_Management/', views.StaffManagement, name = 'Staff_Management'),
   path('Customer_Management/', views.CustomerManagement, name = 'Customer_Management'),
   path('Service_Request/', views.ServicRequest, name = 'Service_Request'),
   path('Rent_Request/', views.RentRequest, name = 'Rent_Request'),
   path('Buy_Request/', views.BuyRequest, name = 'Buy_Request'),
   path('Selling_Request/', views.SellingRequest, name = 'Selling_Request'),
   path('Service_History/', views.ServicHistory, name = 'Service_History'),
   path('Rent_History/', views.RentHistory, name = 'Rent_History'),
   path('Buy_History/', views.BuyHistory, name = 'Buy_History'),
   path('Selling_History/', views.SellingHistory, name = 'Selling_History'),
   path('Notification/', views.Notification, name = 'Notification'),
   path('Profile/', views.Profile, name = 'Profile'),
   path('Error',views.error, name='Error'),
   path('Approve_Admin_Request/<str:role>/<str:email>/', views.ApproveAdminRequest, name='Approve_Admin_Request'),
   path('Remove_Admin_Request/<str:role>/<str:email>/', views.RemoveAdminRequest, name='Remove_Admin_Request'),
   path('Remove_User/<str:role>/<str:email>/', views.RemoveUser, name='Remove_User'),
   path('Approve_Service_Request/<int:id>/', views.ApproveServiceRequest, name='Approve_Service_Request'),
   path('Reject_Service_Request/<int:id>/', views.RejectServiceRequest, name='Reject_Service_Request'),
   path('Approve_Rent_Request/<int:id>/', views.ApproveRentRequest, name='Approve_Rent_Request'),
   path('Remove_Rent_Request/<int:id>/', views.RemoveRentRequest, name='Remove_Rent_Request'),
   path('Approve_Buy_Request/<int:id>/', views.ApproveBuyRequest, name='Approve_Buy_Request'),
   path('Remove_Buy_Request/<int:id>/', views.RemoveBuyRequest, name='Remove_Buy_Request'),
   path('Approve_Selling_Request/<int:id>/', views.ApproveSellingRequest, name='Approve_Selling_Request'),
   path('Remove_Selling_Request/<int:id>/', views.RemoveSellingRequest, name='Remove_Selling_Request'),
]