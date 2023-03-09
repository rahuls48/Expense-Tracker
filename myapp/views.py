from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import datetime
# Create your views here.
def index(request):
    if request.method =="POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()
    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))
    # logic to calculate 365 days expenses
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    yearly_data = Expense.objects.filter(date__gt =last_year)
    yearly_sum = yearly_data.aggregate(Sum('amount'))

    # logic to calculate monthly expenses
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    monthly_data = Expense.objects.filter(date__gt =last_month)
    monthly_sum = monthly_data.aggregate(Sum('amount'))

    #logic to calculate montly expenses
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    weekly_data = Expense.objects.filter(date__gt =last_week)
    weekly_sum = weekly_data.aggregate(Sum('amount'))

    #filter the expenses based on date
    daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))

    #filter the expenses as per category
    categorical_sums = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
    print(categorical_sums)

    expense_form = ExpenseForm()
    #passing contexts to use them and display them in the index.html page
    return render(request,'myapp/index.html',{'expense_form':expense_form,'expenses':expenses,'total_expenses':total_expenses,'yearly_sum':yearly_sum, 'monthly_sum':monthly_sum, 'weekly_sum':weekly_sum,'daily_sums':daily_sums,'categorical_sums':categorical_sums})


def edit(request, id):
    expense = Expense.objects.get(id=id) #this takes the already created objects based on id
    expense_form =ExpenseForm(instance=expense) #we are passing those objects as an instance to the edit form from here
    #For Submit button
    if request.method == "POST":
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index') # after editing it redirects to index.html page

    return render(request,'myapp/edit.html',{'expense_form':expense_form})

def delete(request, id):
    # this checks the delete name which mentioned in the form of delete this done to distinguish the different POST forms
    # There are 2 POST methods edit and delete
    if request.method == "POST" and "delete" in request.POST:
        expense =Expense.objects.get(id=id)
        expense.delete()
    return redirect('index') #after deleting it redirects to index.html page