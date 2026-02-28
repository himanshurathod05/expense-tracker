from django.shortcuts import render, redirect
from .models import Expense, Budget
from .forms import ExpenseForm, BudgetForm
from django.db.models import Sum

# Create your views here.
def dashboard(request):
    expenses = Expense.objects.all()
    total_spent = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    budget_obj = Budget.objects.first()
    total_budget = budget_obj.total_budget if budget_obj else 0
    remaining = total_budget - total_spent

    context = {
        'expenses': expenses,
        'total_spent': total_spent,
        'total_budget': total_budget,
        'remaining': remaining
    }
    return render(request, 'dashboard.html', context)

def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})


def set_budget(request):
    budget_obj = Budget.objects.first()

    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget_obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BudgetForm(instance=budget_obj)

    return render(request, 'set_budget.html', {'form': form})

def view_expenses(request):
    expenses = Expense.objects.all()
    return render(request, 'view_expenses.html', {'expenses': expenses})