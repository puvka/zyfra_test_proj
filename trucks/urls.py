from django.urls import path
from . import views

urlpatterns = [
    path('', views.TruckListView.as_view(), name='truck_list'),
    path('<int:truck_id>/ship/', views.ShipCargoFromTruckView.as_view(), name='ship_cargo_from_truck'),
]
