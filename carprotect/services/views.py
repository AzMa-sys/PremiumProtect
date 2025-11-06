from http.client import HTTPResponse

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import CarBrand, CarModel, CarElement, PriceConfig, Profile
from .forms import CalculatorForm
import json


class HomeView(View):
    def get(self, request):
        brands = CarBrand.objects.all()
        elements = CarElement.objects.all()
        form = CalculatorForm()
        # auto = CarModel.objects.get(pk=brand_id)
        return render(request, 'templates/home.html', {
            'brands': brands,
            'elements': elements,
            'form': form,
            # 'auto': auto
        })


def load_all_prices(request):
    car_model_id = request.GET.get('car_model_id')

    if car_model_id:
        # Загружаем цены для обеих услуг
        tinting_prices = PriceConfig.objects.filter(
            car_model_id=car_model_id,
            service_type='tinting'
        ).select_related('element')

        armor_prices = PriceConfig.objects.filter(
            car_model_id=car_model_id,
            service_type='armor'
        ).select_related('element')

        price_data = {}

        # Добавляем цены тонировки
        for price_config in tinting_prices:
            price_data[str(price_config.element.id)] = {
                'name': price_config.element.name,
                'tinting_price': float(price_config.price),
                'armor_price': 0,
                'element_type': price_config.element.element_type,
                'code': price_config.element.code
            }

        # Добавляем/обновляем цены бронирования
        for price_config in armor_prices:
            element_id = str(price_config.element.id)
            if element_id in price_data:
                price_data[element_id]['armor_price'] = float(price_config.price)
            else:
                price_data[element_id] = {
                    'name': price_config.element.name,
                    'tinting_price': 0,
                    'armor_price': float(price_config.price),
                    'element_type': price_config.element.element_type,
                    'code': price_config.element.code
                }

        return JsonResponse(price_data)

    return JsonResponse({})


def calculate_combined_total(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            car_model_id = data.get('car_model_id')
            selected_tinting_elements = data.get('selected_tinting_elements', [])
            selected_armor_elements = data.get('selected_armor_elements', [])

            total_price = 0
            tinting_total = 0
            armor_total = 0
            tinting_prices = []
            armor_prices = []

            # Расчет тонировки
            for element_id in selected_tinting_elements:
                price_config = PriceConfig.objects.filter(
                    car_model_id=car_model_id,
                    element_id=element_id,
                    service_type='tinting'
                ).first()

                if price_config:
                    tinting_prices.append({
                        'name': price_config.element.name,
                        'price': float(price_config.price)
                    })
                    tinting_total += price_config.price

            # Расчет бронирования
            for element_id in selected_armor_elements:
                price_config = PriceConfig.objects.filter(
                    car_model_id=car_model_id,
                    element_id=element_id,
                    service_type='armor'
                ).first()

                if price_config:
                    armor_prices.append({
                        'name': price_config.element.name,
                        'price': float(price_config.price)
                    })
                    armor_total += price_config.price

            total_price = tinting_total + armor_total

            return JsonResponse({
                'total_price': float(total_price),
                'tinting_total': float(tinting_total),
                'armor_total': float(armor_total),
                'tinting_prices': tinting_prices,
                'armor_prices': armor_prices
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def load_car_models(request):
    brand_id = request.GET.get('brand_id')
    models = CarModel.objects.filter(brand_id=brand_id)
    return JsonResponse(list(models.values('id', 'name', 'tinting', 'protect')), safe=False)


def load_elements_prices(request):
    car_model_id = request.GET.get('car_model_id')
    service_type = request.GET.get('service_type')

    prices = PriceConfig.objects.filter(
        car_model_id=car_model_id,
        service_type=service_type
    ).select_related('element')

    price_data = {}
    for price_config in prices:
        price_data[price_config.element.code] = {
            'name': price_config.element.name,
            'price': float(price_config.price),
            'element_type': price_config.element.element_type
        }

    return JsonResponse(price_data)


def calculate_total(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_elements = data.get('selected_elements', [])
        car_model_id = data.get('car_model_id')
        service_type = data.get('service_type')

        try:
            car_model = CarModel.objects.get(id=car_model_id)
            total_price = car_model.tinting

            # Получаем цены для выбранных элементов
            price_configs = PriceConfig.objects.filter(
                car_model_id=car_model_id,
                service_type=service_type,
                element__code__in=selected_elements
            )

            elements_prices = []
            for config in price_configs:
                elements_prices.append({
                    'name': config.element.name,
                    'price': float(config.price)
                })
                total_price += config.price

            return JsonResponse({
                'total_price': float(total_price),
                'base_price': float(car_model.tinting),
                'elements_prices': elements_prices
            })

        except CarModel.DoesNotExist:
            return JsonResponse({'error': 'Car model not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def about(request):

    data = {
        'profile': Profile.objects.get(id=1),
    }
    return render(request, 'templates/about.html', data)