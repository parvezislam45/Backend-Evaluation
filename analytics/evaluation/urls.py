from django.urls import path
from .views import SalesOverTimeView, SalesGrowthRateView, NewCustomersView, RepeatCustomerListCreate, GeographicalDistributionView, CustomerLifetimeValueView

urlpatterns = [
    path('sales-over-time/', SalesOverTimeView.as_view(), name='sales-over-time'),
    path('sales-growth-rate/', SalesGrowthRateView.as_view(), name='sales-growth-rate'),
    path('new-customers/', NewCustomersView.as_view(), name='new-customers'),
    path('repeat-customers/', RepeatCustomerListCreate.as_view(), name='repeat-customers'),
    path('geographical-distribution/', GeographicalDistributionView.as_view(), name='geographical-distribution'),
    path('customer-lifetime-value/', CustomerLifetimeValueView.as_view(), name='customer-lifetime-value'),
]