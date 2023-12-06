from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('driver/', views.driver, name="driver"),
    path('bus/', views.bus, name="bus"),
    path('add_driver/', views.add_driver, name='add_driver'),
    path('add_bus/', views.add_bus, name='add_bus'),
    path('add_request/', views.add_request, name='add_request'),
    path('request/', views.request, name='request'),
    path('add_schedule/', views.add_schedule, name='add_schedule'),
    path('view_schedule/', views.view_schedule, name='view_schedule'),
    path('delete_driver/<str:id>',views.delete_driver,name='delete_driver'),
    path('delete_bus/<str:id>',views.delete_bus,name='delete_bus'),
    path('delete_schedule/<str:id>',views.delete_schedule,name='delete_schedule'),
    path('add_wallet/', views.add_wallet, name='add_wallet'),
    path('book_bus/', views.book_bus, name='book_bus'),
    path('booking/<int:id>', views.booking, name='booking'),
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/<slug:data>', views.schedule, name='scheduledata'),
    path('home/', views.home, name='home'),
    path('view_booking/', views.view_booking, name='view_booking'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('cancel_booking/<str:id>',views.cancel_booking,name='cancel_booking'),
    path('update_schedule/<int:id>',views.update_schedule,name='update_schedule'),

    
]
