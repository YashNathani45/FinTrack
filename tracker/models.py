# finance_tracker/tracker/models.py

from django.db import models
from django.contrib.auth.models import User

class IncomeSource(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income_sources')

    def __str__(self):
        return self.name

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_categories')

    def __str__(self):
        return self.name

class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(IncomeSource, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')

    def __str__(self):
        return f"{self.amount} from {self.category.name} on {self.date}"

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')

    def __str__(self):
        return f"{self.amount} for {self.category.name} on {self.date}"
