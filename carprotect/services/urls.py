# services/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('ajax/load-models/', views.load_car_models, name='load_models'),
    path('ajax/load-all-prices/', views.load_all_prices, name='load_prices'),
    path('ajax/calculate-combined-total/', views.calculate_combined_total, name='calculate'),
]