from django.shortcuts import render,redirect
from django.views import View
from . forms import *
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

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
        return render(request, 'dashboard.html')
