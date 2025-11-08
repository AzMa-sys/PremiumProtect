from django.db import models


class CarBrand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Марка автомобиля")
    logo = models.ImageField(upload_to='brand_logos/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Марка автомобиля"
        verbose_name_plural = "Марки автомобилей"


class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, verbose_name="Марка")
    name = models.CharField(max_length=100, verbose_name="Модель")
    price_increase = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Повышение цены")
    # prot =  models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="id")


    def __str__(self):
        return f"{self.brand.name} {self.name}"

    class Meta:
        verbose_name = "Модель автомобиля"
        verbose_name_plural = "Модели автомобилей"


class CarElement(models.Model):
    ELEMENT_TYPES = [
        ('windshield', 'Лобовое стекло'),
        ('front_side', 'Передние боковые'),
        ('rear_side', 'Задние боковые'),
        ('rear_window', 'Заднее стекло'),
        ('headlights', 'Фары'),
        ('taillights', 'Задние фонари'),
        ('full_car', 'Полный автомобиль'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название элемента")
    element_type = models.CharField(max_length=20, verbose_name="Тип элемента")
    code = models.CharField(max_length=50, unique=True, verbose_name="Код элемента")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Элемент автомобиля"
        verbose_name_plural = "Элементы автомобиля"


class PriceConfig(models.Model):
    SERVICE_TYPES = [
        ('tinting', 'Тонировка'),
        ('armor', 'Бронирование'),

    ]

    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name="Модель автомобиля")
    element = models.ForeignKey(CarElement, on_delete=models.CASCADE, verbose_name="Элемент")
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, verbose_name="Тип услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"{self.car_model} - {self.element} - {self.get_service_type_display()}"

    class Meta:
        verbose_name = "Настройка цены"
        verbose_name_plural = "Настройки цен"
        unique_together = ['car_model', 'element', 'service_type']


class ServiceType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание")
    code = models.CharField(max_length=50, unique=True, verbose_name="Код услуги")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип услуги"
        verbose_name_plural = "Типы услуг"


class Profile(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя мастера')
    phone = models.CharField(max_length=17, verbose_name='Номер телефона')
    e_mail = models.CharField(max_length=255, verbose_name='email')
    address = models.CharField(max_length=255, verbose_name='Адресс')
    time_w = models.CharField(max_length=255, verbose_name='Часы работы')