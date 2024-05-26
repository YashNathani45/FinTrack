# finance_tracker/tracker/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Income, Expense, IncomeSource, ExpenseCategory  # Import IncomeSource and ExpenseCategory

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['date', 'amount', 'category', 'description']
        widgets = {
            'category': forms.Select(choices=[]),  # Empty choices for now, will be populated dynamically
            'date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = IncomeSource.objects.none()  # Initialize as empty queryset

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'amount', 'category', 'description']
        widgets = {
            'category': forms.Select(choices=[]),  # Empty choices for now, will be populated dynamically
            'date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = ExpenseCategory.objects.none()  # Initialize as empty queryset
