from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.costumer_record, name='record'),
    path('delete_costumer/<int:pk>', views.delete_costumer, name='delete_costumer'),
    path('add_record/', views.add_record, name='add_record'),
    path('stars/', views.stars, name='stars'),
    path('update_costumer/<int:pk>', views.update_costumer, name='update_costumer'),
]
