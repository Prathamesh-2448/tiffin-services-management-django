from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import F, Sum, Q, Count, F, DateTimeField
from django.db.models.functions import TruncMonth
from django.db.models.expressions import Value
from django.db.models.functions import Cast
from .models import Customers, MealOptions, Extras, daily_records
from members.middlewares import auth
import json



@auth
def home(request):
    cust_names = Customers.objects.all()
    Meals = MealOptions.objects.all()
    Extra = Extras.objects.all()
    meal_price = None
    extras_data = []

    if request.method == 'GET':
        return render(request, 'index.html', {'cust_names': cust_names, 'meals':Meals, 'extra':Extra})

    if request.method == 'POST':
        name = request.POST.get('selection')
        date = request.POST.get('mealdate')
        meal_selected = request.POST.get('meal_selected')

        # extras_with_quantity = {}

        selected_extras = []  # Store selected extras
        selected_extras = request.POST.getlist('extras_taken')  # Get selected checkboxes
        # extras_quantities = request.POST.getlist('extras_quantity')  # Get corresponding quantities

        ordered_extras_str = request.POST.get("ordered_extras", "")  # Get the selected extras
        ordered_extras = ordered_extras_str.split(",")  # Convert to list of selected extras

        ordered_quantities_str = request.POST.get("ordered_quantities", "")  # Get the corresponding quantities
        ordered_quantities = ordered_quantities_str.split(",")  # Convert to list of quantities

        print(ordered_quantities_str)
        print(ordered_quantities)
        try:
            # Fetch the meal price from the model
            meal_option = MealOptions.objects.get(MealName=meal_selected)
            meal_price = meal_option.MealPrice  # Extract price
        except MealOptions.DoesNotExist:
            meal_price = "Meal not found"

        # Calculate total extras cost
        total_extras_cost = 0
        for i in range(len(selected_extras)):
            try:
                extra_obj = Extras.objects.get(ExtraName=ordered_extras[i])
                total_extras_cost += extra_obj.ExtraPrice * int(ordered_quantities[i])
                print(extra_obj.ExtraPrice)
            except Extras.DoesNotExist:
                pass  # Skip if extra not found

        total_price = meal_price + total_extras_cost  # Final price

        daily_order = daily_records(
                customer_name=name,
                meal_date = date,
                meal_selected=meal_selected,
                meal_price=meal_price,
                extras_taken=ordered_extras_str,
                extras_quantities=ordered_quantities_str,
                extras_total_price = total_extras_cost,
                total_price=total_price
            )
        daily_order.save()

        if daily_order:
            messages.success(request,f"{name}'s Data Saved Successfully")
        else:
            messages.error(request, "oops! Something went wrong")


        return render(request, 'index.html', {'cust_names': cust_names,'meals':Meals,'extra':Extra})

    else:
        return render(request, 'index.html', {'cust_names': cust_names, 'meals':Meals,'extra':Extra})

@auth
def monthly(request):
    cust_names = Customers.objects.all()

    if request.method == 'GET':
        return render(request, 'monthly.html', {'cust_names': cust_names})

    if request.method == 'POST':
        selected_name = request.POST.get('name')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        data = daily_records.objects.filter(
            customer_name=selected_name,  # Filter by customer name
            meal_date__range=(from_date, to_date))

        try:
            cust_data = Customers.objects.get(address=selected_name)
        except Customers.DoesNotExist:
            cust_data = "No address found!"

        total_price_sum = data.aggregate(Sum('total_price'))['total_price__sum']

        return render(request, 'monthly.html', {'cust_names': cust_names,
                                                'cust_data': data,
                                                'selected_name': selected_name,
                                                'cust_address': cust_data,
                                                'from_date': from_date,
                                                'to_date': to_date,
                                                'total_price_sum': total_price_sum})

    else:
        return render(request, 'monthly.html', {'cust_names': cust_names})

# Analysis View Function
@auth
def dashboard_view(request):
    # Total sales by date
    sales_by_date = (
        daily_records.objects.values('meal_date')
        .annotate(total_sales=Sum('total_price'))
        .order_by('meal_date')
    )
    dates = [record['meal_date'].strftime('%Y-%m-%d') for record in sales_by_date]
    total_sales = [record['total_sales'] for record in sales_by_date]

    #sales_by_month
    sales_by_month = (
        daily_records.objects
        .annotate(meal_datetime=Cast('meal_date', output_field=DateTimeField()))  # Convert DateField to DateTimeField
        .annotate(month=TruncMonth('meal_datetime'))  # Truncate to month
        .values('month')
        .annotate(total_sales=Sum('total_price'))
        .order_by('month')
    )

    months = [record['month'].strftime('%Y-%m') for record in sales_by_month]
    monthly_sales = [record['total_sales'] for record in sales_by_month]

    # Total sales by meal
    sales_by_meal = (
        daily_records.objects.values('meal_selected')
        .annotate(total_sales=Sum('total_price'))
        .order_by('-total_sales')
    )
    meal_names = [record['meal_selected'] for record in sales_by_meal]
    meal_sales = [record['total_sales'] for record in sales_by_meal]

    #sales by address
    # 1. Aggregate sales by customer name:
    sales_by_customer = (
        daily_records.objects
        .values('customer_name')
        .annotate(total_sales=Sum('total_price'))
        .order_by('-total_sales')
    )

    # 2. Create a dictionary to map customer names to addresses:
    customer_addresses = {}
    for customer in Customers.objects.all():  # Iterate through Customers table
        customer_addresses[customer.name] = customer.address

    # 3. Aggregate sales by address using the mapping:
    sales_by_address = {}
    for record in sales_by_customer:
        customer_name = record['customer_name']
        total_sales = record['total_sales']
        address = customer_addresses.get(customer_name)  # Get address, handle missing customers

        if address:  # Only include records with known addresses
            if address in sales_by_address:
                sales_by_address[address] += total_sales
            else:
                sales_by_address[address] = total_sales

    address_list = list(sales_by_address.keys())
    address_sales = list(sales_by_address.values())

    print(address_list)

    context = {
        'dates': json.dumps(months, ensure_ascii=False),
        'total_sales': json.dumps(monthly_sales, ensure_ascii=False),
        'meal_names': json.dumps(address_list, ensure_ascii=False),
        'meal_sales': json.dumps(address_sales, ensure_ascii=False),
    }
    return render(request, 'dashboard.html', context)

@auth
def add_customers(request):
    list_custName = Customers.objects.all()


    context = {
        'list_cust':list_custName,
    }
    if request.method == 'POST':
        if 'save' in request.POST:
            name = request.POST.get('name')
            number = request.POST.get('number')
            address = request.POST.get('address')



            new_cust_info = Customers(
                name=name,
                number=number,
                address=address,
            )

            new_cust_info.save()
            return render(request, 'add-customer.html', context)

        if 'search' in request.POST:
            searched = request.POST.get('searched')
            search_result = Customers.objects.filter(Q(name__icontains=searched)| Q(number__icontains=searched) | Q(address__icontains=searched))

            if not search_result:
                messages.success(request, 'No Search Results Found!')
            return render(request, 'add-customer.html', {'search_result': search_result})

    else:
        return render(request, 'add-customer.html', context)