from datetime import date
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from order.models import Order
from .forms import OrderForm, BikeItemFormSet, AccessoryItemFormSet
from django.db.models import Sum
from decimal import Decimal, InvalidOperation

def create_order(request):
    if not request.user.is_authenticated:
        return render(request, 'order_message.html')
    
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        bike_formset = BikeItemFormSet(request.POST)
        accessory_formset = AccessoryItemFormSet(request.POST)

        try:
            if order_form.is_valid() and (bike_formset.is_valid() or accessory_formset.is_valid()):
                start_date = order_form.cleaned_data['start_date']
                end_date = order_form.cleaned_data['end_date']

                errors = []
                errors.extend(check_equipment_availability(bike_formset, start_date, end_date))
                errors.extend(check_equipment_availability(accessory_formset, start_date, end_date))

                if errors:
                    return render(request, 'create-order.html', {
                        'order_form': order_form,
                        'bike_formset': bike_formset,
                        'accessory_formset': accessory_formset,
                        'errors': errors
                    })

                order = order_form.save(commit=False)
                order.order_date = date.today()
                order.user = request.user

                total_cost = calculate_total_cost(bike_formset, accessory_formset, start_date, end_date)
                order.total_cost = total_cost
                order.save()

                bike_formset.instance = order
                bike_formset.save()
                accessory_formset.instance = order
                accessory_formset.save()

                return redirect('home')
            else:
                return render(request, 'create-order.html', {
                    'order_form': order_form,
                    'bike_formset': bike_formset,
                    'accessory_formset': accessory_formset
                })

        except Exception as e:
            return render(request, 'create-order.html', {
                'order_form': order_form,
                'bike_formset': bike_formset,
                'accessory_formset': accessory_formset,
                'errors': [f"An unexpected error occurred: {e}"]
            })
    else:
        order_form = OrderForm()
        bike_formset = BikeItemFormSet()
        accessory_formset = AccessoryItemFormSet()

    return render(request, 'create-order.html', {
        'order_form': order_form,
        'bike_formset': bike_formset,
        'accessory_formset': accessory_formset
    })

def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        order_form = OrderForm(request.POST, instance=order)
        bike_formset = BikeItemFormSet(request.POST, instance=order)
        accessory_formset = AccessoryItemFormSet(request.POST, instance=order)

        if order_form.is_valid() and bike_formset.is_valid() and accessory_formset.is_valid():
            start_date = order_form.cleaned_data['start_date']
            end_date = order_form.cleaned_data['end_date']

            errors = []
            errors.extend(check_equipment_availability(bike_formset, start_date, end_date))
            errors.extend(check_equipment_availability(accessory_formset, start_date, end_date))

            if errors:
                return render(request, 'edit_order.html', {
                    'order_form': order_form,
                    'bike_formset': bike_formset,
                    'accessory_formset': accessory_formset,
                    'order': order,
                    'errors': errors
                })

            try:
                total_cost = calculate_total_cost(bike_formset, accessory_formset, start_date, end_date)
                if total_cost is None or total_cost < 0:
                    raise InvalidOperation("Invalid total cost calculated.")
            except InvalidOperation as e:
                return render(request, 'edit_order.html', {
                    'order_form': order_form,
                    'bike_formset': bike_formset,
                    'accessory_formset': accessory_formset,
                    'order': order,
                    'errors': [f"Error calculating total cost: {e}"]
                })

            order = order_form.save(commit=False)
            order.total_cost = total_cost
            order.save()

            bike_formset.instance = order
            bike_formset.save()
            accessory_formset.instance = order
            accessory_formset.save()

            return redirect('user')
    else:
        order_form = OrderForm(instance=order)
        bike_formset = BikeItemFormSet(instance=order)
        accessory_formset = AccessoryItemFormSet(instance=order)

        order_form.fields['start_date'].widget.attrs['readonly'] = True
        order_form.fields['end_date'].widget.attrs['readonly'] = True

    return render(request, 'edit_order.html', {
        'order_form': order_form,
        'bike_formset': bike_formset,
        'accessory_formset': accessory_formset,
        'order': order
    })


def check_equipment_availability(formset, start_date, end_date):
    errors = []
    for i, item in enumerate(formset.cleaned_data):
        if item:
            equipment = item['equipment']
            requested_quantity = item['quantity']

            reserved_quantity = (
                formset.model.objects.filter(
                    equipment=equipment,
                    order__start_date__lt=end_date,
                    order__end_date__gt=start_date
                )
                .aggregate(total_reserved=Sum('quantity'))['total_reserved'] or 0
            )

            available_quantity = equipment.quantity - reserved_quantity

            if requested_quantity > available_quantity:
                formset[i].add_error(
                    'quantity',
                    f"{equipment.name} is not available in sufficient quantity "
                    f"({requested_quantity} requested, {available_quantity} available) "
                    f"between {start_date} and {end_date}."
                )
                errors.append(f"{equipment.name} - insufficient stock.")
    return errors


def calculate_total_cost(bike_formset, accessory_formset, start_date, end_date):
    rental_days = (end_date - start_date).days
    print(rental_days)

    li = {
        1: lambda price: price,
        2: lambda price: round(price * Decimal('0.90'), 2),
        3: lambda price: round(price * Decimal('0.85'), 2),
        4: lambda price: round(price * Decimal('0.80'), 2),
        5: lambda price: round(price * Decimal('0.70'), 2),
        6: lambda price: round(price * Decimal('0.65'), 2)
    }

    def calculate_item_cost(item, rental_days):
        price_for_one_day = item['equipment'].price_for_one_day
        total_item_cost = 0

        for day in range(1, rental_days + 1):
            if day <= 5:
                total_item_cost += li[day](price_for_one_day)
            else:
                total_item_cost += li[6](price_for_one_day)
        
        return total_item_cost

    total_cost = 0
    for bike_item in bike_formset.cleaned_data:
        if bike_item:
            total_cost += bike_item["quantity"] * calculate_item_cost(bike_item, rental_days)

    for accessory_item in accessory_formset.cleaned_data:
        if accessory_item:
            total_cost += accessory_item["quantity"] * calculate_item_cost(accessory_item, rental_days)

    return total_cost

def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('user')

    return render(request, 'delete_order.html', {'order': order})
