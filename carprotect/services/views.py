# services/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import CarBrand, CarModel, PriceConfig, Profile
import json


class HomeView(View):
    def get(self, request):
        brands = CarBrand.objects.all()
        return render(request, 'templates/home.html', {
            'brands': brands,
        })


def load_car_models(request):
    brand_id = request.GET.get('brand_id')
    if not brand_id:
        return JsonResponse([], safe=False)
    models = CarModel.objects.filter(brand_id=brand_id).values('id', 'name')
    return JsonResponse(list(models), safe=False)


def load_all_prices(request):
    car_model_id = request.GET.get('car_model_id')
    if not car_model_id:
        return JsonResponse({})

    tinting = PriceConfig.objects.filter(
        car_model_id=car_model_id, service_type='tinting'
    ).select_related('element')
    armor = PriceConfig.objects.filter(
        car_model_id=car_model_id, service_type='armor'
    ).select_related('element')

    data = {}
    for pc in tinting:
        eid = str(pc.element.id)
        data[eid] = data.get(eid, {
            'name': pc.element.name,
            'tinting_price': 0,
            'armor_price': 0,
            'element_type': pc.element.element_type,
            'code': pc.element.code
        })
        data[eid]['tinting_price'] = float(pc.price)

    for pc in armor:
        eid = str(pc.element.id)
        data[eid] = data.get(eid, {
            'name': pc.element.name,
            'tinting_price': 0,
            'armor_price': 0,
            'element_type': pc.element.element_type,
            'code': pc.element.code
        })
        data[eid]['armor_price'] = float(pc.price)

    return JsonResponse(data)


def calculate_combined_total(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        payload = json.loads(request.body)
        car_model_id = payload.get('car_model_id')
        tinting_ids = payload.get('selected_tinting_elements', [])
        armor_ids = payload.get('selected_armor_elements', [])

        if not car_model_id:
            return JsonResponse({'error': 'No car model'}, status=400)

        tinting_total = armor_total = 0
        tinting_items = []
        armor_items = []

        for eid in tinting_ids:
            pc = PriceConfig.objects.filter(
                car_model_id=car_model_id,
                element_id=eid,
                service_type='tinting'
            ).first()
            if pc:
                price = float(pc.price)
                tinting_items.append({'name': pc.element.name, 'price': price})
                tinting_total += price

        for eid in armor_ids:
            pc = PriceConfig.objects.filter(
                car_model_id=car_model_id,
                element_id=eid,
                service_type='armor'
            ).first()
            if pc:
                price = float(pc.price)
                armor_items.append({'name': pc.element.name, 'price': price})
                armor_total += price

        return JsonResponse({
            'total_price': tinting_total + armor_total,
            'tinting_total': tinting_total,
            'armor_total': armor_total,
            'tinting_prices': tinting_items,
            'armor_prices': armor_items
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def about(request):
    profile = Profile.objects.get(id=1)
    return render(request, 'templates/about.html', {'profile': profile})