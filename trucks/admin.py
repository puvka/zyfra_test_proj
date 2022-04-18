from django.contrib import admin
from . import models


@admin.register(models.TruckModel)
class TruckModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Truck)
class TruckAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Cargo)
class CargoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ShipmentLog)
class ShipmentLogAdmin(admin.ModelAdmin):
    pass
