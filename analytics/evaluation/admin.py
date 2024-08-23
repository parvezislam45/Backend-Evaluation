from django.contrib import admin
from .models import Customers,Product,Order,SalesData,SalesGrowth,Address,Repeat

admin.site.register([Customers,Product,Order,SalesData,SalesGrowth,Address,Repeat])
