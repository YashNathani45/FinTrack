"""
URL configuration for finance_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# finance_tracker/finance_tracker/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tracker import views as tracker_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',tracker_views.home,name='home'),
    path('add_income/', tracker_views.add_income, name='add_income'),
    path('all_incomes/', tracker_views.all_incomes, name='all_incomes'),
    path('all_expense/', tracker_views.add_expense, name='all_expense'),
    path('all_expenses/', tracker_views.all_expenses, name='all_expenses'),

     path('transactions/delete/<int:transaction_id>/', tracker_views.delete_transaction, name='delete_transaction'),
     path('delete-income/<int:income_id>/', tracker_views.delete_income, name='delete_income'), 
     path('delete-expense/<int:income_id>/', tracker_views.delete_expense, name='delete_expense'),


    path('dashboard/', tracker_views.dashboard, name='dashboard'),
    path('all_transactions/', tracker_views.all_transactions, name='all_transactions'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='tracker/logout.html'), name='logout'),
    path('register/', tracker_views.register, name='register'),
    
    path('tracker/', include('tracker.urls')),  # Include the tracker app's URLs

]
