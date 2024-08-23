from django.db.models import Sum, Count, F, Q
from django.db.models.functions import TruncDay, TruncMonth, TruncQuarter, TruncYear
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.utils import timezone
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Customers,Product,SalesGrowth,SalesData,Repeat
from .serializers import CustomerSerializer,ProductSerializer,OrderSerializer,SalesDataSerializer,SalesGrowthSerializer,RepeatCustomerSerializer

# View to handle posting data and returning the calculated results
class OrderListCreate(APIView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request, *args, **kwargs):
        order_data = request.data
        # Assuming validation and data processing here
        Order.objects.create(**order_data)
        return Response({"message": "Order created successfully"}, status=status.HTTP_201_CREATED)
    
class RepeatCustomerListCreate(APIView):
    def get(self, request, *args, **kwargs):
        repeats = Repeat.objects.all()
        serializer = RepeatCustomerSerializer(repeats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = RepeatCustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Total Sales Over Time
class SalesOverTimeView(APIView):
    def get(self, request, *args, **kwargs):
        interval = request.query_params.get('interval', 'monthly')
        sales_data = SalesData.objects.filter(interval=interval)
        serializer = SalesDataSerializer(sales_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = SalesDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Sales Growth Rate Over Time
class SalesGrowthRateView(APIView):
    def get(self, request, *args, **kwargs):
        interval = request.query_params.get('interval', 'monthly')
        growth_data = SalesGrowth.objects.filter(interval=interval)
        serializer = SalesGrowthSerializer(growth_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = SalesGrowthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# New Customers Added Over Time
class NewCustomersView(APIView):
    def get(self, request, *args, **kwargs):
        interval = request.query_params.get('interval', 'monthly')
        now = datetime.now()

        if interval == 'daily':
            start_date = make_aware(now - timedelta(days=1))
        elif interval == 'weekly':
            start_date = make_aware(now - timedelta(weeks=1))
        elif interval == 'monthly':
            start_date = make_aware(now - timedelta(days=30))
        elif interval == 'yearly':
            start_date = make_aware(now - timedelta(days=365))
        else:
            return Response({'error': 'Invalid interval'}, status=status.HTTP_400_BAD_REQUEST)

        customers = Customers.objects.filter(created_at__gte=start_date)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Number of Repeat Customers
class RepeatCustomersView(APIView):
    def get(self, request, *args, **kwargs):
        interval = request.query_params.get('interval', 'monthly')
        
        # Define the date range based on the interval
        today = timezone.now().date()
        if interval == 'daily':
            start_date = today - timedelta(days=1)
            end_date = today
        elif interval == 'monthly':
            start_date = today.replace(day=1) - timedelta(days=1)
            end_date = today.replace(day=1)
        elif interval == 'quarterly':
            start_date = today - timedelta(days=90)  # Approximation
            end_date = today
        elif interval == 'yearly':
            start_date = today - timedelta(days=365)  # Approximation
            end_date = today
        else:
            start_date = today
            end_date = today

        # Filter orders based on the date range and count the orders
        repeat_customers = Customers.objects.annotate(
            order_count=Count('order', filter=Q(order__created_at__range=[start_date, end_date]))
        ).filter(order_count__gt=1)

        serializer = CustomerSerializer(repeat_customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Geographical Distribution of Customers
class GeographicalDistributionView(APIView):
    def get(self, request, *args, **kwargs):
        geo_data = Customers.objects.values('default_address__city').annotate(customer_count=Count('id'))
        return Response(geo_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Customer Lifetime Value by Cohorts
class CustomerLifetimeValueView(APIView):
    def get(self, request, *args, **kwargs):
        cohort_data = Customers.objects.annotate(cohort_month=TruncMonth('created_at')).values('cohort_month').annotate(lifetime_value=Sum('order__total_price')).order_by('cohort_month')
        return Response(cohort_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)