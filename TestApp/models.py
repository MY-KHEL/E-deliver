
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from datetime import datetime, time, timezone
import secrets
from django.urls import reverse
from .paystack import Paystack 
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    address=models.TextField(max_length=2000)
    phone_number= PhoneNumberField()
    image = models.ImageField(upload_to='upload',blank=True,null=True)

class Dispatch(models.Model):
    first_name=models.CharField(max_length=80)
    last_name=models.CharField(max_length=80)
    username = models.CharField(max_length=80,unique=True,)
    id=models.CharField(primary_key=True, max_length=80)
    
   
    def __str__(self):
        return self.username
    

class DeliveryForm(models.Model):
    receiver_first_name= models.CharField(max_length=80)
    receiver_last_name= models.CharField(max_length=80)
    receiver_phone_number = PhoneNumberField()
    mail = models.ForeignKey('Mail', on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)


class Mail(models.Model):
    STATUS=[
        ('Not_Assigned','Not_Assigned'),
        ('Assigned','Assigned'),
        ('Delivered','Delivered')
    ]
    first_name=models.CharField(max_length=80)
    last_name=models.CharField(max_length=80)
    Phone_Number=PhoneNumberField()
    Sender_Address=models.CharField(max_length=1000,null=True,blank=True) 
    sender_city = models.ForeignKey('City',on_delete=models.CASCADE,related_name='sender_city')
    recipent_first_name=models.CharField(max_length=80)
    recipent_last_name=models.CharField(max_length=80)
    recipent_phone_number=PhoneNumberField()
    Address=models.TextField('Recipent Address',max_length=1000)
    receiver_city = models.ForeignKey('City',on_delete=models.CASCADE,related_name='receiver_city')
    status = models.CharField(max_length=20,choices=STATUS,default='Not_Assigned')
    timestamp = models.DateTimeField(default=datetime.now)
    picked = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.recipent_first_name} {self.recipent_last_name} -- {self.id}'

    def __price__(self):
        return(self.receiver_city['Price'])

    @property
    def del_info(self):
        return DeliveryForm.objects.filter(mail=self)
    
class AssignMail(models.Model):
    STATUS=[
    ('Assigned','Assigned'),
    ('Delivered','Delivered')
    ]
    mailid = models.ForeignKey(Mail,on_delete=models.CASCADE)
    riderid = models.ForeignKey(Dispatch,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=20,choices=STATUS,default='Assigned')

  
    
    @property
    def get_dispatch(self):
        return Dispatch.objects.get(id=self.riderid)

class Payment(models.Model):
    amount=models.PositiveIntegerField(blank=True)
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)  
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['-date']

    def __str__(self) -> str:
        return f'Payment: {self.amount}'

    def save(self,*args, **kwargs)-> None:
        while not self.ref: 
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref=Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref=ref
        super().save(*args, **kwargs)
    
    def amount_value(self) -> int:
        return self.amount*100

    def verify_payment(self):
        paystack = Paystack()
        status,result = paystack.verify_payment(self.ref,self.amount)
        if status:
            if result['amount']/100==self.amount:
                self.verified=True
            self.save()
        if self.verified:
            return True 
        return False      
# class ReceiveMail(models.Model):
#     RATING=[
#         ('Excellent','Excellent'),
#         ('Very Good','Very Good'),
#         ('Good','Good'),
#         ('Fair','Fair'),
#         ('Poor','Poor'),
#     ]
#     first_name=models.CharField(max_length=80)
#     last_name = models.CharField(max_length=80)
#     phone_number=models.CharField(max_length=80)
#     mailid = models.ForeignKey(Mail,on_delete=models.CASCADE,default=True)
#     dispatch_rating=models.CharField(max_length=80,choices=RATING) 
#     timestamp = models.DateTimeField(auto_now_add=True)
    

class Complaint(models.Model):
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=90)
    email = models.EmailField()
    complaint = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)

    def get_absolute_url(self):
        return reverse("read_comment", kwargs={"id": self.id})

# class Verify(models.Model):
#     mail = models.ForeignKey(Mail,on_delete=)

class City(models.Model):
    Name = models.CharField(unique=True,max_length=300)
    Price = models.PositiveIntegerField(default=1000)
    
    def __str__(self): 
        return self.Name
     
    def __price__(self):
        return self.Price

