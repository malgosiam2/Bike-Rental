from django.shortcuts import render
from .forms import EquipmentFilterForm
from .models import Bike, Accessory
from decimal import Decimal

def price_offer_view(request):
    bikes = Bike.objects.all()
    accessories = Accessory.objects.all()

    bike_prices = []
    for bike in bikes:
        price_for_one_day = bike.price_for_one_day
        bike_prices.append({
            'bike': bike,
            'price_2nd_day': round(price_for_one_day * Decimal('0.90'), 2),
            'price_3rd_day': round(price_for_one_day * Decimal('0.85'), 2),
            'price_4th_day': round(price_for_one_day * Decimal('0.80'), 2),
            'price_5th_day': round(price_for_one_day * Decimal('0.70'), 2),
            'price_6th_plus_day': round(price_for_one_day * Decimal('0.65'), 2),
        })

    accessory_prices = []
    for acc in accessories:
        price_for_one_day = acc.price_for_one_day
        accessory_prices.append({
            'accessory': acc,
            'price_2nd_day': round(price_for_one_day * Decimal('0.90'), 2),
            'price_3rd_day': round(price_for_one_day * Decimal('0.85'), 2),
            'price_4th_day': round(price_for_one_day * Decimal('0.80'), 2),
            'price_5th_day': round(price_for_one_day * Decimal('0.70'), 2),
            'price_6th_plus_day': round(price_for_one_day * Decimal('0.65'), 2),
        })

    return render(request, "price_offer.html", {
        'bike_prices': bike_prices,
        'accessory_prices': accessory_prices
    })

def offer_view(request):
    bikes = Bike.objects.all()
    accessories = Accessory.objects.all()

    form = EquipmentFilterForm(request.GET)

    if form.is_valid():
        sort_by = form.cleaned_data.get('sort_by')
        if sort_by == 'price_asc':
            bikes = bikes.order_by('price_for_one_day')
            accessories = accessories.order_by('price_for_one_day')
        elif sort_by == 'price_desc':
            bikes = bikes.order_by('-price_for_one_day')
            accessories = accessories.order_by('-price_for_one_day')
        elif sort_by == 'az_asc':
            bikes = bikes.order_by('bike_type')
            accessories = accessories.order_by('accessory_type')
        elif sort_by == 'az_desc':
            bikes = bikes.order_by('-bike_type')
            accessories = accessories.order_by('-accessory_type')

    return render(request, "offer.html", {'bikes': bikes, 'accessories': accessories, 'form': form})


