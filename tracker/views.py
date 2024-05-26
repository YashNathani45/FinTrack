# finance_tracker/tracker/views.py

# finance_tracker/tracker/views.py


from django.contrib.auth import login, authenticate
from django.http import HttpResponse, JsonResponse
from flask import Flask, jsonify, render_template
from .forms import UserRegisterForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm, ExpenseForm
from .models import Income, Expense
from .models import IncomeSource,ExpenseCategory
from django.db.models import Sum
# finance_tracker/tracker/views.py
from flask_cors import CORS
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Income, Expense, IncomeSource, ExpenseCategory
from django.contrib.auth.models import User
app= Flask(__name__)


def home(request):
    return render(request, 'tracker/homepage.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'tracker/register.html', {'error': 'Username already exists'})
            elif User.objects.filter(email=email).exists():
                return render(request, 'tracker/register.html', {'error': 'Email already exists'})
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                login(request, user)
                return redirect('dashboard')
        else:
            return render(request, 'tracker/register.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'tracker/register.html')

@login_required
def dashboard(request):
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    transactions = sorted(
        list(incomes) + list(expenses),
        key=lambda x: x.date,
        reverse=True
    )
    for transaction in transactions:
        if isinstance(transaction, Income):
            transaction.transaction_type = 'Income'
        else:
            transaction.transaction_type = 'Expense'
    context = {
        'transactions': transactions,
    }
    return render(request, 'tracker/dashboard.html', context)

from .models import Income

from django.shortcuts import render
from .models import Income
@login_required
def all_transactions(request):
    # Fetch all incomes and expenses for the current user
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    # Combine incomes and expenses into a single list and sort by date
    transactions = list(incomes) + list(expenses)
    transactions.sort(key=lambda x: x.date, reverse=True)  # Sort by date in descending order

    return render(request, 'tracker/transactions.html', {'transactions': transactions})
@login_required
def add_income(request):
    # Fetch all incomes for the current user
    incomes = Income.objects.filter(user=request.user).order_by('-date') 
    
    # If it's a POST request, process the form data
    if request.method == 'POST':
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        category_name = request.POST.get('category')
        description = request.POST.get('description')

        category, created = IncomeSource.objects.get_or_create(name=category_name, user=request.user)
        Income.objects.create(
            user=request.user,
            date=date,
            amount=amount,
            category=category,
            description=description
        )

    # Render the add_income.html template with the incomes
    return render(request, 'tracker/addincome.html', {'incomes': incomes})


@login_required
def all_incomes(request):
    # Fetch all incomes for the current user
    incomes = Income.objects.filter(user=request.user)
    
    # Render the template with the incomes
    return render(request, 'tracker/allincomes.html', {'incomes': incomes})
@login_required
def all_expenses(request):
    # Fetch all incomes for the current user
    expenses = Expense.objects.filter(user=request.user)
    
    # Render the template with the incomes
    return render(request, 'tracker/allexpense.html', {'expenses': expenses})
@login_required
def add_expense(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date') 
    if request.method == 'POST':
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        category_name = request.POST.get('category')
        description = request.POST.get('description')

        category, created = ExpenseCategory.objects.get_or_create(name=category_name, user=request.user)
        Expense.objects.create(
            user=request.user,
            date=date,
            amount=amount,
            category=category,
            description=description
        )
        
    return render(request, 'tracker/addexpense.html', {'expenses': expenses})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'tracker/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'tracker/login.html')

import json
from decimal import Decimal
from collections import defaultdict
from calendar import month_abbr
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tracker.models import Income, Expense
from datetime import datetime

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

@login_required
def dashboard(request):
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    total_income = sum(income.amount for income in incomes)
    total_expenses = sum(expense.amount for expense in expenses)
    savings = total_income - total_expenses

    # Initialize data for all months
    income_data = {month: 0 for month in month_abbr[1:]}
    expense_data = {month: 0 for month in month_abbr[1:]}

    # Group data by month
    for income in incomes:
        month = income.date.month
        income_data[month_abbr[month]] += float(income.amount)

    for expense in expenses:
        month = expense.date.month
        expense_data[month_abbr[month]] += float(expense.amount)

    print("Income Data:", income_data)  # Debug statement
    print("Expense Data:", expense_data)  # Debug statement

    return render(request, 'tracker/dashboard.html', {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': savings,
        'income_data': json.dumps(income_data, default=decimal_to_float),
        'expense_data': json.dumps(expense_data, default=decimal_to_float),
    })


def delete_income(request, income_id):
    income = get_object_or_404(Income, pk=income_id)
    income.delete()
    return redirect('add_income')
def delete_expense(request, income_id):
    expense = get_object_or_404(Expense, pk=income_id)
    expense.delete()
    return redirect('add_expense')
from django.shortcuts import redirect

def delete_transaction(request, transaction_id):
    try:
        # Check if the transaction exists as an income
        income_transaction = Income.objects.get(pk=transaction_id)
        income_transaction.delete()
        return redirect('all_transactions')  # Redirect to the all_transactions page
    except Income.DoesNotExist:
        try:
            # Check if the transaction exists as an expense
            expense_transaction = Expense.objects.get(pk=transaction_id)
            expense_transaction.delete()
            return redirect('all_transactions')  # Redirect to the all_transactions page
        except Expense.DoesNotExist:
            return HttpResponse('Transaction not found', status=404)



