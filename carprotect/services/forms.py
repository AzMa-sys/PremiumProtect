from django import forms

from .models import CarBrand, CarModel


class CalculatorForm(forms.Form):
    car_brand = forms.ModelChoiceField(
        queryset=CarBrand.objects.all(),
        empty_label="Выберите марку",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'car-brand'})
    )

    car_model = forms.ModelChoiceField(
        queryset=CarModel.objects.none(),
        empty_label="Сначала выберите марку",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'car-model'})
    )

    service_type = forms.ChoiceField(
        choices=[
            ('tinting', 'Тонировка'),
            ('armor', 'Бронирование'),
            ('both', 'Тонировка + Бронирование'),
        ],
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'service-type'})
    )