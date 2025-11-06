from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('ajax/load-models/', views.load_car_models, name='ajax_load_models'),
    path('ajax/load-prices/', views.load_elements_prices, name='ajax_load_prices'),
    path('ajax/calculate-total/', views.calculate_total, name='ajax_calculate_total'),
    path('ajax/load-all-prices/', views.load_all_prices, name='ajax_load_all_prices'),
    path('ajax/calculate-combined-total/', views.calculate_combined_total, name='ajax_calculate_combined_total'),
    path('about/',views.about, name='about'),
]