from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import *

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model= CustomUser
    add_form = signupForm
    fieldsets = (
        *UserAdmin.fieldsets, 
        (
            'Extra Information',
            {
                 "fields": 
                [
                    'image',
                    'phone_number',
                    'address'
                    ]
                ,
            }
           
        ),
    )

admin.site.register(Dispatch)
admin.site.register(AssignMail)
admin.site.register(Mail)
admin.site.register(DeliveryForm)
admin.site.register(Payment)
admin.site.register(City)

admin.site.register(CustomUser, CustomUserAdmin)