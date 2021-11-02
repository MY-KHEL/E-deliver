from django.contrib.auth import login
from django.http import response
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .models import *
from twilio.rest import Client

from .forms import *
import json
from pypaystack import Transaction,Customer,Plan
from django.http import JsonResponse
# Create your views here.
@login_required
def decide(request):
    if request.user.is_superuser:
        return redirect('home')
    else:
        return redirect('dispatch')


def home(request):
    uuser = CustomUser.objects.get(id=request.user.id)

    
    mail_list=Mail.objects.filter(status='Not_Assigned').order_by('-pk')[:5]
    mail=Mail.objects.all()
    mail_list2=Mail.objects.filter(status='Not_Assigned').order_by('-pk')
    mail_list_count=mail.count()
    mail_assigned = Mail.objects.filter(status='Assigned') 
    mail_assigned_count =mail_assigned.count()
    mail_delivered = DeliveryForm.objects.all()
    
  
    mail_deliver = Mail.objects.filter(status='Delivered')
    mailid=None
    for item in mail_deliver:
        mailid=item.id
        
    # get_the_mail_delivered = ReceiveMail.objects.filter(other_id=mailid)
    # print(get_the_mail_delivered)
    mail_delivered_count=mail_deliver.count()
    

    context={
        'mail_list':mail_list,
        'mail_list2':mail_list2,
        'mail_list_count':mail_list_count,
        'mail_assigned_count':mail_assigned_count,
        'mail_delivered_count':mail_delivered_count,
        'mail_delivered':mail_delivered,
        'uuser':uuser,
        
    }
    return render(request,'index.html',context)

def get_dispatch():
    detail = CustomUser.objects.filter(is_superuser=False)
    for det in detail:
        first_name = det.first_name
        last_name = det.last_name
        id = det.id
        username = det.username
        register = Dispatch.objects.get_or_create(first_name=first_name,last_name=last_name,username=username,id=id)
        

def signup(request):
    form = signupForm(request.POST or None,request.FILES or None)
    if request.method=='POST':
        form = signupForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            get_dispatch()
            return redirect('home')
        
    else:
        form=signupForm()

    context={
        'form':form
    }
    return render(request,'registration/signup.html',context)

def dispatchManagement(request):
    items = CustomUser.objects.filter(is_superuser=False)
    item2 = Dispatch.objects.all()
    context={
        'items':items,
        'item2':item2
    }
    return render(request,'dispatchmgt.html',context)

def assign(request,pk):
    mail=Mail.objects.get(id=pk)
    rider = Dispatch.objects.all()

    context ={
        'mail':mail,
        'rider':rider
    }
    return render(request,'mail/assignmail.html',context)

def add_mail(request):
    form = MailForm(request.POST or None)
    if request.method =='POST':
        form=MailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
           
    else:
        form = MailForm()
    
    context={
        'form':form
    }
    return render(request,'mail/addmail.html',context)

def assign_to_dispatch(request,pk,userid):
    mail = Mail.objects.get(id=pk)
    rider = Dispatch.objects.get(id=userid)
    riderid=rider.id
    mailid=mail.id
   
    assign = AssignMail.objects.get_or_create(mailid=mail,riderid=rider)

    mail.status = 'Assigned'
    mail.save()
    
    return redirect('home')


def dispatch_home(request):
    rider_id = request.user.id
    #print(rider_id)
    get_mail = AssignMail.objects.filter(riderid=rider_id)
    #print(get_mail)
    get_mail_count = get_mail.count() 
    delivered = []
    for item in get_mail:
        if item.status=='Delivered':
            delivered.append(item)
            
    delivered_count=(len(delivered))
    yet_delivered_count= get_mail_count-delivered_count
    context ={
    'get_mail':get_mail,
    'get_mail_count':get_mail_count,
    'delivered_count':delivered_count,
    'yet_delivered_count':yet_delivered_count

    }
    return render(request,'dispatch/dispatch.html',context)



def dispatch_mail(request):
    rider_id = request.user.id
    get_mail = AssignMail.objects.filter(riderid=rider_id).order_by('-timestamp')
    get_mail_count = get_mail.count() 

    delivered = []
    for item in get_mail:
        if item.status=='Delivered':
            delivered.append(item)
            
    delivered_count=(len(delivered))
    yet_delivered_count= get_mail_count-delivered_count

    get_last_mail = AssignMail.objects.filter(riderid=rider_id).order_by('-timestamp')[:1]

   
    rider = Dispatch.objects.get(id=rider_id)
    mail =Mail.objects.all()
   

    context ={
        'get_mail':get_mail,
        'mail':mail,
        'rider':rider,
        'get_last_mail':get_last_mail,
        'yet_delivered_count':yet_delivered_count,
        

    }
    
    return render (request,'dispatch/mail.html',context)

def dispatch_read_mail(request,riderid,mailid):
    mail= Mail.objects.get(id=mailid)
    mail_assigned = AssignMail.objects.filter(riderid=riderid).order_by('-timestamp')
    get_mail = AssignMail.objects.get(mailid=mail.id)
    get_mail_count = mail_assigned.count() 

    delivered = []
    for item in mail_assigned:
        if item.status=='Delivered':
            delivered.append(item)
            
    delivered_count=(len(delivered))
    yet_delivered_count= get_mail_count-delivered_count
          
    rider = Dispatch.objects.get(id=riderid)

    
    context ={
        'get_mail':get_mail,
        'rider':rider,
        'mail':mail,
        'mail_assigned':mail_assigned,
        'yet_delivered_count':yet_delivered_count,
        

    }

    return render(request,'dispatch/read_mail.html',context)

   
def deliver_mail(request,pk):
    mail = Mail.objects.get(id=pk)
    
    mail2 = Mail.objects.filter(id=pk)

    
    
    get_mail = AssignMail.objects.get(mailid=pk)
    
    form = Deliver(request.POST or None )
    if request.method == 'POST':
        form = Deliver(request.POST,initial={'mail':mail})
        if form.is_valid():
            form.save()
            
            account = settings.TWILIO_ACCOUNT_SID
            token = settings.TWILIO_AUTH_TOKEN
            number = settings.TWILIO_PHONE_NUMBER
            phone = +15005550006
            print(phone)
            client = Client(account, token)
            message = client.messages.create(to=number, from_= phone,
                                            body="Hello there!") 

            mail.status = 'Delivered'
            mail.save()
            get_mail.status = 'Delivered'
            get_mail.save()
            return redirect('dispatch_mail')
    else:
        form = Deliver(initial={'mail':mail})



    context={
        'mail':mail,
        'form':form
    }
    return render(request,'dispatch/deliver.html',context)



            

def managemails(request):
    mail = AssignMail.objects.filter(status='Assigned')
    mail2 = Mail.objects.all()

    paginator = Paginator(mail2, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={
     'mail':mail,   
     'mail2':mail2,
     'page_obj': page_obj   
    }
    return render(request,'mail/managemail.html',context )
def reassignmail(request,pk):
    mail= AssignMail.objects.get(id=pk)
    order = Mail.objects.get(id=pk)
    form = Reassign(request.POST or None)

    if request.method =='POST':
        form = Reassign(request.POST,instance=mail)
        
        if form.is_valid():
            form.save()
        return redirect('home')
    else:
        form=Reassign(instance=mail)
    context={
        'mail':mail,
        'form':form
    }
    return render(request,'mail/reassign.html',context)
def mailinfo(request,pk):
    mail = DeliveryForm.objects.get(id=pk)
    
    dispatch = AssignMail.objects.get(id=pk)


    context={
        'mail':mail,
        'dispatch':dispatch

    }
    return render(request, 'mail/info.html',context)


# def verify_payment(request:HttpRequest,ref:str) -> HttpResponse:
#     payment = get_object_or_404(Payment,ref=ref)
#     verified = payment.verify_payment()
#     

def land_page(request):
    return render(request,'landpage.html')
def verify(request,id):
    transaction = Transaction(authorization_key=settings.PAYSTACK_SECRET_KEY)
    response = transaction.verify(id)
    data = JsonResponse(response,safe=False)
    if response:
        return redirect('landpage')
    return(data)
def pickupservice(request):

    
    form = PickupMailForm(request.POST or None)
    payment_form = PaymentForm(request.POST or None)
    city=None
    get_city=None
    city_price=None
    if request.method =='POST':
        form=PickupMailForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['receiver_city']
            get_city = City.objects.get(Name=city)
            city_price = get_city.Price
            form.save()

        payment_form = PaymentForm(request.POST,initial={'amount':city_price})
        if payment_form.is_valid():
            payment = payment_form.save() 
           
            
            return render(request, 'payment/make_payment.html', {'payment':payment,'payment_form':payment_form,'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})

           
        else:
            payment_form=PaymentForm(initial={'amount':city_price}) 
        return render(request,'payment/initiate_payment.html',{'payment_form':payment_form})
    
        
    else:
        
        form = PickupMailForm()

    context={
        'form':form
    }
    return render(request,'pickupservice.html',context)
def payment(request):
    payment_form = PaymentForm(request.POST or None)
    if request.method=='POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request, 'payment/make_payment.html', {'payment':payment,'payment_form':payment_form,'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})
        else:
            payment_form=PaymentForm() 
    return(request,'payment/initiate_payment.html',{'payment_form':payment_form})
def initiate_payment(request: HttpRequest):
    
    return()


   
def subscribe(request):
    email = request.POST["email"]
    subject = 'Thanks For your Complaints'
    message = 'Edeliver really appreciates your complaint and will work on it as soon as possible. '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )

    return()    
def write_comments(request):
    form = ComplaintForm(request.POST or None)
    if request.method=='POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            subscribe(request)
            return redirect('landpage')
    else:
        form=ComplaintForm()
    context={
        'form':form,
    }
    return render(request,'comments.html',context)
def check_comments(request):
    comments = Complaint.objects.all()
    paginator = Paginator(comments, 7)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context={
        'comments':comments,
        'page_obj': page_obj 
    }
    return render(request,'view_comments.html',context)

def read_comment(request,id):
    comments =  Complaint.objects.get(id=id)

    context={
     'comments':comments,   
    }
    return render(request,'read_comment.html',context)

def update_profile(request,id):
    dispatch = CustomUser.objects.get(id=id)
    rider = Dispatch.objects.get(id=id)
    form = signupForm(request.POST,request.FILES or None)
    if request.method=='POST':
        form = signupForm(request.POST,request.FILES,instance=dispatch)
        if form.is_valid():
              
            form.save()
            
            # firstname=signupForm.cleaned_data.get('first_name')
            # lastname=signupForm.cleaned_data.get('last_name')
            # username=signupForm.cleaned_data.get('username')

            # rider.first_name = firstname
            
            # rider.last_name = lastname
         
            # rider.username=username
            # rider.save()
            return redirect('dispatch')
    else:
        form = signupForm(instance=dispatch)

    context={
        'form':form
    }
    return render(request,'dispatch/update_profile.html',context)

def add_city(request):
    city_form = CityForm(request.POST or None)
    if request.method=='POST':
        city_form = CityForm(request.POST)
        if city_form.is_valid():
            city_form.save()
            return redirect('addmail')
    else:
        city_form=CityForm()
    context={
        'form':city_form
    }           
    return render(request,'mail/addcity.html',context)