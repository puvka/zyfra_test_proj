from django.contrib.gis.geos import Point

from core.use_cases import base
from trucks import models
from trucks.models import Stock


class ShipCargoFromTruck(base.UseCase):
    """
        Выгрузка на склад
    """

    def __init__(self, *, truck: models.Truck, x_coord: int, y_coord: int):
        self.truck = truck
        self.x_coord = x_coord
        self.y_coord = y_coord

    def execute(self) -> models.ShipmentLog:
        point = Point(self.x_coord, self.y_coord)
        is_success = True
        cargo_extras = None

        cargo = self.truck.cargo

        stock = Stock.objects.filter(geom__intersects=point).first()
        if not stock:
            stock = Stock.objects.first()
            is_success = False

        actual_stock_balance = stock.balance

        if is_success:
            actual_stock_balance += cargo.volume
            cargo_extras = cargo.extras

            stock.balance = actual_stock_balance
            stock.save(update_fields=['balance'])

            cargo.volume = 0
            cargo.extras = None
            cargo.save(update_fields=['volume', 'extras'])

        shipment_log = models.ShipmentLog.objects.create(
            stock=stock,
            truck=self.truck,
            balance_before=stock.balance,
            balance_after=actual_stock_balance,
            cargo_extras=cargo_extras,
            pnt=point
        )

        return shipment_log
