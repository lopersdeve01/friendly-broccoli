"""oldbeast URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from insects import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login,name='login'),
    url(r'^register/$', views.register,name='register'),
    url(r'^home/', views.home, name='home'),
    url(r'^customers/', views.Customers.as_view(), name='customers'),
    url(r'^customer/', views.customer, name='customer'),
    url(r'^mycustomer/', views.customer, name='mycustomer'),
    url(r'^editcustomer/(\d+)', views.edit, name='editcustomer'),
    url(r'^addcustomer/', views.add, name='addcustomer'),

    url(r'^start/', views.start, name='start'),
    # url(r'^add/', views.addedit, name='add'),
    # url(r'^edit/(\d+)', views.addedit, name='edit'),
    # url(r'^addedit/(\d+)/', views.addedit, name='addedit'),
    url(r'^delete/(\d+)/', views.delete, name='delete'),
    url(r'^choose/', views.choose, name='choose'),
    url(r'^query/', views.query, name='query'),
    url(r'^value/', views.value, name='value'),
]
