from django.contrib.gis.db import models


class TruckModel(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    cargo_capacity = models.PositiveSmallIntegerField(
        verbose_name='Макс. грузоподъемность',
        help_text='Измеряется в тоннах'
    )

    class Meta:
        verbose_name = 'Модель грузовика'
        verbose_name_plural = 'Модели грузовиков'


class Truck(models.Model):
    model = models.ForeignKey(TruckModel, on_delete=models.PROTECT)
    site_number = models.CharField(verbose_name='Бортовой номер', max_length=100)

    class Meta:
        verbose_name = 'Грузовик'
        verbose_name_plural = 'Грузовики'
        unique_together = (('model', 'site_number'),)

    def __str__(self):
        return self.site_number


class Cargo(models.Model):
    truck = models.OneToOneField(Truck, on_delete=models.CASCADE)

    volume = models.PositiveSmallIntegerField(
        verbose_name='текущий вес', help_text='Измеряется в тоннах'
    )
    extras = models.JSONField(verbose_name='Доп.данные о грузе', null=True)

    class Meta:
        verbose_name = 'Текущий груз грузовика'
        verbose_name_plural = 'Текущий груз грузовиков'

    @property
    def overload_volume(self) -> float:
        """
            Значение перегруза грузовика
        """
        max_val = self.truck.model.cargo_capacity
        overload = max(self.volume - max_val, 0)
        return round(overload * 100 / max_val, 1)


class Stock(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    geom = models.PolygonField(verbose_name='Область склада')
    balance = models.PositiveIntegerField(verbose_name='Остаток на складе', default=0)

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.name


class ShipmentLog(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete=models.PROTECT)

    pnt = models.PointField(verbose_name='Координаты выгрузки')
    balance_before = models.PositiveSmallIntegerField(
        verbose_name='Объем до разгрузки', help_text='Измеряется в тоннах'
    )
    balance_after = models.PositiveSmallIntegerField(
        verbose_name='Объем после разгрузки',
        help_text='Измеряется в тоннах'
    )

    cargo_extras = models.JSONField(verbose_name='Доп. данные о грузе', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')

    class Meta:
        verbose_name = 'Журнал разгрузки'
        verbose_name_plural = 'Журнал разгрузки'
