from django.shortcuts import render,redirect
from django.views import View
from . forms import *
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.db.models import Sum

class RegisterView(View):
    def get(self,request,*args,**kwargs):
        form=RegForm()
        return render(request, 'register.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = RegForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            print(request.user)
            return redirect('dashboard')
        return render(request, 'register.html', {'form': form})
            
class DashboardView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        
        transactions = Transaction.objects.all().order_by('-date')[:5]
        goals = Goal.objects.filter(user=request.user)
        trfilter = Transaction.objects.filter(user=request.user)
        
        total_income = Transaction.objects.filter(user=request.user,transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = Transaction.objects.filter(user=request.user,transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
        net_savings = total_income-total_expense
        
        context = {
            'trfilter':trfilter,
            'total_income':total_income,
            'total_expense':total_expense,
            'transactions':transactions,
            'net_savings':net_savings
        }
        return render(request, 'dashboard.html',context)
    
class TransactionCreateView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        form = TransactionForm()
        return render(request, 'transaction.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction=form.save(commit=False)
            transaction.user = request.user
            transaction.save()   
            return redirect('dashboard')
        print(form.errors)           
        return render(request, 'transaction.html', {'form': form})
    
class GoalCreateView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        form = GoalForm()
        return render(request, 'goal_form.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = GoalForm(request.POST)
        if form.is_valid():
            goal=form.save(commit=False)
            goal.user = request.user
            goal.save()   
            return redirect('dashboard')
        print(form.errors)           
        return render(request, 'goal_form.html', {'form': form})
    
class TransactionListView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        transactions = Transaction.objects.all().order_by('-date')
        return render(request, 'transactions.html',{'transactions':transactions})
    
    
