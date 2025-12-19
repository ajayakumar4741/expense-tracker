from django.shortcuts import render,redirect
from django.views import View
from . forms import *
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.db.models import Sum
from .admin import *
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required

# def search_transactions(request):
#     query = request.GET.get('q')  # get search term from ?q=...
#     results = []

#     if query:
#         results = Transaction.objects.filter(
#             Q(user=request.user) & (
#                 Q(title__icontains=query) |
#                 Q(transaction_type__icontains=query) |
#                 Q(amount__icontains=query) |
#                 Q(id__icontains=query)
#             )
#         ).order_by('-date')

#     context = {
#         'query': query,
#         'results': results,
#     }
#     return render(request, 'transactions.html', context)


def summarize_expense_data(user):
    expenses = Transaction.objects.filter(user=user, transaction_type='Expense')
    df = pd.DataFrame(list(expenses.values('category','amount')))
    
    if df.empty:
        return None,None
    
    summary = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    categories = summary.index.tolist()
    amounts = summary.values.tolist()
    
    
    return categories, amounts

def get_bar_chart(categories, amounts):
    # Set a non-GUI backend for systems without display servers
    plt.switch_backend('Agg') 
    plt.figure(figsize=(10, 6))
    plt.bar(categories, amounts, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    
    plt.ylabel('Amount')
    plt.tight_layout()

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close() # Close the figure to free memory

    # Encode the image to Base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    
    return image_base64

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
            messages.success(request,'Account Created Successfully !!!')
            return redirect('dashboard')
        return render(request, 'register.html', {'form': form})
            
class DashboardView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        
        categories, amounts = summarize_expense_data(request.user)
        chart_data = None
        if categories and amounts:
            chart_data = get_bar_chart(categories, amounts)
        
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:5]
        goals = Goal.objects.filter(user=request.user)[:5]
        trfilter = Transaction.objects.filter(user=request.user)
        
        total_income = Transaction.objects.filter(user=request.user,transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = Transaction.objects.filter(user=request.user,transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
        net_savings = total_income-total_expense
        
        remaining_savings = net_savings
        goal_progress = []
        for goal in goals:
            if remaining_savings >= goal.target_amount:
                goal_progress.append({'goal':goal,'progress':100})
                remaining_savings -= goal.target_amount
            elif remaining_savings > 0:
                progress = (remaining_savings / goal.target_amount) * 100 # 24488 / 
                goal_progress.append({'goal':goal,'progress':progress})
                remaining_savings = 0
            else:
                goal_progress.append({'goal':goal,'progress':0})
        
        context = {
            'trfilter':trfilter,
            'total_income':total_income,
            'total_expense':total_expense,
            'transactions':transactions,
            'net_savings':net_savings,
            'goal_progress':goal_progress,
            'chart_data':chart_data
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
            messages.success(request,'Transaction added successfully !!!')
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
            messages.success(request,'Goal added successfully !!!')
            return redirect('dashboard')
        print(form.errors)           
        return render(request, 'goal_form.html', {'form': form})
    
class TransactionListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')

        if query:
            transactions = transactions.filter(
                Q(title__icontains=query) |
                Q(transaction_type__icontains=query) |
                Q(amount__icontains=query)
            )

        context = {
            'transactions': transactions,
            'query': query,
        }
        return render(request, 'transactions.html', context)

    
class GoalListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        goals = Goal.objects.filter(user=request.user)

        # Calculate savings
        total_income = Transaction.objects.filter(
            user=request.user, transaction_type='Income'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        total_expense = Transaction.objects.filter(
            user=request.user, transaction_type='Expense'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        net_savings = total_income - total_expense
        remaining_savings = net_savings

        # Build progress list
        goal_progress = []
        for goal in goals:
            if remaining_savings >= goal.target_amount:
                goal_progress.append({'goal': goal, 'progress': 100})
                remaining_savings -= goal.target_amount
            elif remaining_savings > 0:
                progress = (remaining_savings / goal.target_amount) * 100
                goal_progress.append({'goal': goal, 'progress': progress})
                remaining_savings = 0
            else:
                goal_progress.append({'goal': goal, 'progress': 0})

        return render(request, 'goal_list.html', {
            'goal_progress': goal_progress,
            'net_savings': net_savings,
            'total_income': total_income,
            'total_expense': total_expense,
        })
    
def export_transaction(request):
    user_transactions = Transaction.objects.filter(user=request.user)
    
    transaction_resources = TransactionResource()
    dataset = transaction_resources.export(queryset=user_transactions)
    
    excel_data = dataset.export('xlsx')
    response = HttpResponse(excel_data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=transactions_report.xlsx'
    return response

# READ
@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'user_profile.html',{'profile': profile})

# UPDATE
@login_required
def profile_update(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(request, 'profile_update.html', {
        'u_form': u_form,
        'p_form': p_form
    })

# DELETE
@login_required
def profile_delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('login')
    return render(request, 'profile_delete.html')
