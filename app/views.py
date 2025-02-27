from itertools import chain
from django.db.models import Q
from django.http import HttpResponse, request
from django.contrib.auth import login, logout,authenticate
from django.shortcuts import get_object_or_404,redirect, render
from django.contrib import messages
from django.template import context
from django.views import View
from django.views.generic import CreateView,ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .form import *
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from app.models import *
from .filters import *
from .import form
from django.core.paginator import Paginator
from multiselectfield import MultiSelectField,MultiSelectFormField

def search_list(request):
  if request.method == 'POST':
    q = request.POST['q']
    startup_data = StartupInfo.objects.filter(company_name__icontains=q)
    investor_data = Investorinfo.objects.filter(company_name__icontains=q)
    customer_data = CustomerInfo.objects.filter(name__icontains=q)
    data = chain(startup_data,investor_data,customer_data)
    
  context = {'data': data, 'q': q, 'startup_data': startup_data,'investor_data':investor_data,'customer_data':customer_data}
  return render(request,'app/search_list.html',context)


def home(request):
  startup = StartupInfo.objects.all()
  total_startup = startup.count()
  investor = Investorinfo.objects.all()
  total_investor = investor.count()
  customer = CustomerInfo.objects.all()
  total_customer = customer.count()
  
  
  context = {'total_startup': total_startup,
             'total_investor': total_investor, 'total_customer': total_customer,
              'startups':startup,'investors':investor,'customer':customer }
  return render(request,'app/home.html',context)

def about(request):
  return render(request,'app/about.html')

def pricing(request):
  return render(request, 'app/pricing_table.html')

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
    return render(request, 'app/login.html',context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/login')

# def userProfileForm(request,pk):
#   if request.method == "POST":
#     if request.user.is_startup:
#       obj = get_object_or_404(StartupInfo, user_id=request.user.id)
#       form = Startup_profileForm(request.POST, request.FILES, instance=obj)
#     elif request.user.is_investor:
#       obj = get_object_or_404(Investorinfo, user_id=request.user.id)
#       form = Investor_profileForm(request.POST,request.FILES, instance=obj)
#     elif request.user.is_customer:
#       obj = get_object_or_404(CustomerInfo, user_id=request.user.id)
#       form = Customer_profileForm(request.POST, request.FILES, instance=obj)
#     if form.is_valid():
#       messages.success(request, "Profile Updated successfully!!!")
#       form.save()
        
#   else:
#     if request.user.is_startup:
#       form = Startup_profileForm()
#     elif request.user.is_investor:
#       form = Investor_profileForm()
#     elif request.user.is_customer:
#       form = Customer_profileForm()
#   context={'form':form}
  
#   return render(request,'app/user_profileForm.html',context)


class StartUpdateView(LoginRequiredMixin, UpdateView):
  model = StartupInfo
  fields = ('name', 'company_name', 'title', 'email', 'mobile', 'logo', 'establish_year', 'business_model', 'employee_range',
            'market_presence', 'looking_at', 'sector', 'description', 'videofile', 'weblink', 'facebook_link', 'linkedin_link', 'twitter_link', 'location',
            'person1', 'person1_name', 'person1_image', 'person2', 'person2_name', 'person2_image')
  
  template_name = 'app/user_profileForm.html'
  login_url = 'login'

  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if obj.user != self.request.user:
      raise PermissionDenied
    return super().dispatch(request, *args, **kwargs)

class InvestorUpdateView(LoginRequiredMixin, UpdateView):
  model = Investorinfo
  fields = ('name', 'company_name', 'title', 'email', 'mobile', 'logo', 'establish_year', 'investor_type', 'employee_range',
            'market_presence', 'looking_at', 'tags', 'description', 'videos', 'weblink', 'facebook_link', 'linkedin_link', 'twitter_link', 'location',
            'person1', 'person1_name', 'person1_image', 'person2', 'person2_name', 'person2_image')
  template_name = 'app/user_profileForm.html'
  login_url = 'login'

  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if obj.user != self.request.user:
      raise PermissionDenied
    return super().dispatch(request, *args, **kwargs)
class CustomerUpdateView(LoginRequiredMixin, UpdateView):
  model = CustomerInfo
  fields = ('name', 'mobile', 'email', 'profession', 'biography', 'looking_at',
            'sector', 'image', 'facebook_link', 'linkedin_link', 'twitter_link')
  template_name = 'app/user_profileForm.html'
  login_url = 'login'

  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if obj.user != self.request.user:
      raise PermissionDenied
    return super().dispatch(request, *args, **kwargs)

  
def profile(request,pk):
  if request.user.is_startup:
    startup = StartupInfo.objects.get(user_id=request.user.id)
    reviews = ReviewRating.objects.filter(startup_id=startup.id, status=True)
    count = reviews.count()
    return render(request, 'app/startup_profile.html', {'startup': startup, 'reviews': reviews,  'count': count})
  elif request.user.is_investor:
    investor = Investorinfo.objects.get(user_id=request.user.id)
    reviews = InvestorReviewRating.objects.filter(investor_id=investor.id, status=True)
    count = reviews.count()
    return render(request, 'app/investor_profile.html', {'investor': investor, 'reviews': reviews,'count':count})
  elif request.user.is_customer:
    customer = CustomerInfo.objects.get(user_id=request.user.id)
    return render(request, 'app/customer_profile.html', {'customer': customer})


def startup_profile(request, pk):
  startup = StartupInfo.objects.get(pk=pk)
  reviews = ReviewRating.objects.filter(startup_id=startup.id, status=True)
  count = reviews.count()
  thread = ThreadModel.objects.filter(pk=pk)
  message_list = MessageModel.objects.filter(thread__pk__contains=pk)
  return render(request, 'app/startup_profile.html', {'startup': startup, 'reviews': reviews, 'count': count,'thrad':thread ,'message_list': message_list})

def startup_home(request):
  startups = StartupInfo.objects.all()
  myfilter = StartupFilter(request.GET,queryset=startups)
  startups = myfilter.qs
  after_filter = startups.count()
  page = Paginator(startups, per_page=2)
  page_list = request.GET.get('page')
  page = page.get_page(page_list)
  context = {'startups': startups,'page':page,'myfilter': myfilter, 'after_filter': after_filter}
  return render(request, 'app/startup_home.html',context)

def investor_profile(request,pk):
  investor = Investorinfo.objects.get(pk=pk)
  reviews = InvestorReviewRating.objects.filter(investor_id=investor.id, status=True)
  count = reviews.count()
  thread = ThreadModel.objects.filter(pk=pk)
  message_list = MessageModel.objects.filter(thread__pk__contains=pk)
  return render(request, 'app/investor_profile.html', {'investor': investor, 'reviews': reviews, 'count': count,'thread':thread,'message_list':message_list})

def investor_home(request):
  investors = Investorinfo.objects.all()
  myfilter = InvestorFilter(request.GET, queryset=investors)
  investors = myfilter.qs
  after_filter = investors.count()
  page = Paginator(investors, per_page=2)
  page_list = request.GET.get('page')
  page = page.get_page(page_list)
  context = {'investors': investors, 'page':page,'myfilter': myfilter,'after_filter':after_filter}
  return render(request, 'app/investor_home.html',context)




def customer_profile(request,pk):
  customer = CustomerInfo.objects.get(pk=pk)
  return render(request, 'app/customer_profile.html',{'customer':customer})

def customer_home(request):
  customers= CustomerInfo.objects.all()
  myfilter = CustomerFilter(request.GET,queryset=customers)
  customers=myfilter.qs
  count=customers.count()
  page = Paginator(customers,per_page=2)
  page_list=request.GET.get('page')
  page=page.get_page(page_list)
  context={'customers':customers,'page':page,'myfilter':myfilter,'count':count}
  return render(request,'app/customer_home.html',context)


def article(request):
  return render(request, 'app/article.html')



def submit_review(request,startup_id):
  url=request.META.get('HTTP_REFERER')
  if request.method == 'POST':
    try:
      reviews=ReviewRating.objects.get(user_id=request.user.id, startup_id=startup_id)
      form=ReviewForm(request.POST, instance=reviews)
      form.save()
      messages.success(
          request, 'Thank you! Your review has been updated.')
      return redirect(url)
    except ReviewRating.DoesNotExist:
      form=ReviewForm(request.POST)
      if form.is_valid():
          data=ReviewRating()
          data.rating=form.cleaned_data['rating']
          data.review=form.cleaned_data['review']
          data.startup_id=startup_id
          data.user_id=request.user.id
          data.save()
          
          return redirect(url)

def investor_submit_review(request,investor_id):
  url=request.META.get('HTTP_REFERER')
  if request.method == 'POST':
    try:
      reviews=InvestorReviewRating.objects.get(user_id=request.user.id, investor_id=investor_id)
      form=Investor_ReviewForm(request.POST, instance=reviews)
      form.save()
      messages.success(
          request, 'Thank you! Your review has been updated.')
      return redirect(url)
    except InvestorReviewRating.DoesNotExist:
      form=Investor_ReviewForm(request.POST)
      if form.is_valid():
          data=InvestorReviewRating()
          data.rating=form.cleaned_data['rating']
          data.review=form.cleaned_data['review']
          data.investor_id=investor_id
          data.user_id=request.user.id
          data.save()
          
          return redirect(url)


class PostNotification(View):
    def get(self, request, notification_pk, message_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        message = MessageModel.objects.get(pk=message_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('thread', pk=message_pk)


class ThreadNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=object_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('thread', pk=object_pk)


class FollowNotification(View):
  def get(self,request,notification_pk,profile_pk,*args,**kwargs):
    notification = Notification.objects.get(pk=notification_pk)
    if request.user.is_startup:
      profile = StartupInfo.objects.get(pk=profile_pk)
    elif request.user.is_investor:
      profile = Investorinfo.objects.get(pk=profile_pk)
    elif request.user.is_customer:
      profile = CustomerInfo.objects.get(pk=profile_pk)
    notification.user_has_seen = True
    notification.save()
    return redirect('profile' ,pk=profile_pk)

class ThreadNotification(View):
  def get(self,request,notification_pk,object_pk,*args,**kwargs):
    notification = Notification.objects.get(pk=notification_pk)
    if request.user.is_startup:
      thread = ThreadModel.objects.get(pk=object_pk)
    elif request.user.is_investor:
      thread = ThreadModel.objects.get(pk=object_pk)
    elif request.user.is_customer:
      thread = ThreadModel.objects.get(pk=object_pk)
    notification.user_has_seen = True
    notification.save()
    return redirect('thread', pk=object_pk)

class RemoveNotification(View):
  def delete(self, request, notification_pk, profile_pk, *args, **kwargs):
    notification = Notification.objects.get(pk=notification_pk)
    notification.user_has_seen = True
    notification.save()
    return HttpResponse('Success',content_type = 'text/plain')


class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(
            Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, 'app/inbox.html', context)


class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }

        return render(request, 'app/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(
                    user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(
                    user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            messages.error(request, 'Invalid username!!')
            return redirect('create-thread')


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'app/thread.html', context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message')
        )

        message.save()
        notification = Notification.objects.create(

          notification_type = 1,
          from_user = request.user,
          to_user = receiver,
          thread= thread, 
        )

        return redirect('thread', pk=pk)
