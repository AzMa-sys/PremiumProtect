from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Initialize basic data for the calculator'

    def handle(self, *args, **options):
        # Импортируем модели внутри метода, чтобы избежать проблем с настройками
        from services.models import CarBrand, CarModel, CarElement, PriceConfig

        # Создаем базовые элементы автомобиля
        elements_data = [
            {'name': 'Лобовое стекло', 'code': 'windshield', 'element_type': 'windshield'},
            {'name': 'Передние боковые стекла', 'code': 'front_sides', 'element_type': 'front_side'},
            {'name': 'Задние боковые стекла', 'code': 'rear_sides', 'element_type': 'rear_side'},
            {'name': 'Заднее стекло', 'code': 'rear_window', 'element_type': 'rear_window'},
            {'name': 'Передние фары', 'code': 'headlights', 'element_type': 'headlights'},
            {'name': 'Задние фонари', 'code': 'taillights', 'element_type': 'taillights'},
            {'name': 'Все стекла', 'code': 'all_windows', 'element_type': 'full_car'},
        ]

        for element_data in elements_data:
            element, created = CarElement.objects.get_or_create(
                code=element_data['code'],
                defaults=element_data
            )
            if created:
                self.stdout.write(f'Created element: {element.name}')

        # Создаем тестовые марки и модели
        brands_data = [
            {
                'name': 'BMW',
                'models': [
                    {'name': '3 Series', 'base_price': 5000},
                    {'name': '5 Series', 'base_price': 7000},
                    {'name': 'X5', 'base_price': 9000},
                ]
            },
            {
                'name': 'Mercedes-Benz',
                'models': [
                    {'name': 'C-Class', 'base_price': 5500},
                    {'name': 'E-Class', 'base_price': 7500},
                    {'name': 'GLE', 'base_price': 9500},
                ]
            },
            {
                'name': 'Audi',
                'models': [
                    {'name': 'A4', 'base_price': 5200},
                    {'name': 'A6', 'base_price': 7200},
                    {'name': 'Q7', 'base_price': 9200},
                ]
            },
            {
                'name': 'Toyota',
                'models': [
                    {'name': 'Camry', 'base_price': 4500},
                    {'name': 'RAV4', 'base_price': 6000},
                    {'name': 'Land Cruiser', 'base_price': 8500},
                ]
            },
            {
                'name': 'Hyundai',
                'models': [
                    {'name': 'Solaris', 'base_price': 4000},
                    {'name': 'Tucson', 'base_price': 5500},
                    {'name': 'Santa Fe', 'base_price': 7000},
                ]
            }
        ]

        for brand_data in brands_data:
            brand, created = CarBrand.objects.get_or_create(name=brand_data['name'])
            if created:
                self.stdout.write(f'Created brand: {brand.name}')

            for model_data in brand_data['models']:
                model, created = CarModel.objects.get_or_create(
                    brand=brand,
                    name=model_data['name'],
                    defaults={'base_price': model_data['base_price']}
                )
                if created:
                    self.stdout.write(f'Created model: {brand.name} {model.name}')

        # Создаем тестовые цены
        self.stdout.write('Creating price configurations...')
        car_models = CarModel.objects.all()
        elements = CarElement.objects.all()

        price_configs_created = 0
        for car_model in car_models:
            for element in elements:
                # Базовый множитель цены в зависимости от типа элемента
                if element.element_type == 'full_car':
                    price_multiplier = 2.0
                elif element.element_type in ['windshield', 'rear_window']:
                    price_multiplier = 1.5
                else:
                    price_multiplier = 1.0

                # Цены для тонировки
                _, created1 = PriceConfig.objects.get_or_create(
                    car_model=car_model,
                    element=element,
                    service_type='tinting',
                    defaults={'price': car_model.base_price * price_multiplier * 0.3}
                )

                # Цены для бронирования
                _, created2 = PriceConfig.objects.get_or_create(
                    car_model=car_model,
                    element=element,
                    service_type='armor',
                    defaults={'price': car_model.base_price * price_multiplier * 0.5}
                )

                # Цены для комплекса
                _, created3 = PriceConfig.objects.get_or_create(
                    car_model=car_model,
                    element=element,
                    service_type='both',
                    defaults={'price': car_model.base_price * price_multiplier * 0.7}
                )

                if created1 or created2 or created3:
                    price_configs_created += 1

        self.stdout.write(f'Created {price_configs_created} price configurations')
        self.stdout.write(self.style.SUCCESS('Successfully initialized basic data!'))
        self.stdout.write('You can now:')
        self.stdout.write('1. Access the admin panel at /admin/')
        self.stdout.write('2. Use the calculator at /')
        self.stdout.write('3. Add more cars and prices through the admin panel')