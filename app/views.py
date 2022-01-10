from django.shortcuts import render
from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import View
from django.views.generic import CreateView
from .form import *
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from app.models import *



def home(request):
  startup = StartupInfo.objects.all()
  total_startup = startup.count()
  investor = Investorinfo.objects.all()
  total_investor = investor.count()
  customer = CustomerInfo.objects.all()
  total_customer = customer.count()
  context = {'total_startup': total_startup,
             'total_investor': total_investor, 'total_customer': total_customer, }
  return render(request,'app/home.html',context)


def register(request):
    return render(request, 'app/register.html')


class customer_register(View):
  def get(self, request):
    form = CustomersignUpForm()
    return render(request, 'app/customer_register.html', {'form': form})

  def post(self, request):
    form = CustomersignUpForm(request.POST)
    if form.is_valid():
      messages.success(request, "Congratulations!!! Registered successfully")
      form.save()
    return redirect('/login')
class startup_register(View):
  def get(self, request):
    form = StartupsignUpForm()
    return render(request, 'app/startup_register.html', {'form': form})

  def post(self, request):
    form = StartupsignUpForm(request.POST)
    if form.is_valid():
      messages.success(request, "Congratulations!!! Registered successfully")
      form.save()
    return redirect('/login')
class investor_register(View):
  def get(self, request):
    form = InvestorsignUpForm()
    return render(request, 'app/investor_register.html', {'form': form})

  def post(self, request):
    form = InvestorsignUpForm(request.POST)
    if form.is_valid():
      messages.success(request, "Congratulations!!! Registered successfully")
      form.save()
    # return render(request, 'app/investor_register.html', {'form': form})
    return redirect('/login')

# class customer_register(CreateView):
#     model = User
    
#     form_class = CustomersignUpForm
#     template_name = 'app/customer_register.html'

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('/')

# class investor_register(CreateView):
#     model = User
#     form_class = InvestorsignUpForm
#     template_name = 'app/employee_register.html'

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('/')
# class startup_register(CreateView):
#     model = User
#     form_class = StartupsignUpForm
#     template_name = 'app/employee_register.html'

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('/login')


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, 'app/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/login')

def userProfileForm(request):
  if request.method == "POST":
    if request.user.is_startup:
      form = Startup_profileForm(request.POST)
    elif request.user.is_investor:
      form = Investor_profileForm(request.POST)
    else:
      form = Customer_profileForm(request.POST)
    if form.is_valid():
      form.save()
      if request.user.is_startup:
        form = Startup_profileForm()
      elif request.user.is_investor:
        form = Investor_profileForm()
      else:
        form = Customer_profileForm()
      messages.success(request,"Profile Updated successfully!!!")
  else:
    if request.user.is_startup:
      form = Startup_profileForm()
    elif request.user.is_investor:
      form = Investor_profileForm()
    else:
      form = Customer_profileForm()
  context={'form':form}
  
  return render(request,'app/user_profileForm.html',context)
  