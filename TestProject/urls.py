"""TestProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
#from django.urls.conf import include
from django.conf.urls.static import static
from TestApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('decide',decide,name='decide'),
    path('home', home , name='home'),
    path('dispatch/', dispatch_home , name='dispatch'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup , name='signup'),
    path('addmail/', add_mail , name='addmail'),
    path('dispatchManagement/', dispatchManagement , name='dispatchManagement'),
    path('assign/<int:pk>/', assign , name='assign'),
    path('reassign/<int:pk>/', reassignmail , name='reassign'),
    path('deliver/<int:pk>/', deliver_mail , name='deliver'),
    path('mailinfo/<int:pk>/', mailinfo, name='mailinfo'),
    path('assign_to_dispatch/<int:pk>/<int:userid>/', assign_to_dispatch,name='assign_to_dispatch'),
    path('dispatch_mail', dispatch_mail,name='dispatch_mail'),
    path('read_mail/<int:riderid>/<int:mailid>/',dispatch_read_mail,name='read_mail'),
    path('pickupservice', pickupservice , name='pickupservice'),
    path('managemail', managemails , name='managemail'),
    path('initiate_payment', initiate_payment , name='initiate_payment'),
    # path('<str:ref>/',verify_payment ,name='verify_payment'),
    path('verify/<str:id>',verify,name='verify'),
    path('',land_page,name='landpage'),
    path('comments',write_comments,name='comments'),
    path('view_comments',check_comments,name='view_comments'),
    path('read_comment/<int:id>/',read_comment,name='read_comment'),
    path('update_profile/<int:id>/',update_profile,name='update_profile'),
    path('add_city/',add_city,name='add_city')

    
]
if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 