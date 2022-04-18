from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, FormView

from trucks import models
from . import forms
from . import use_cases
from django.contrib import messages


class TruckListView(ListView):
    model = models.Truck
    template_name = 'trucks/truck_list.html'

    def get_queryset(self):
        return super().get_queryset().select_related('cargo', 'model').order_by('site_number')


class ShipCargoFromTruckView(FormView):
    template_name = 'trucks/stock_detail.html'
    form_class = forms.ShipCargoFromTruckForm

    def form_valid(self, form):
        truck = get_object_or_404(models.Truck, pk=self.kwargs.get('truck_id'))

        if truck.cargo.volume == 0:
            messages.info(self.request, f'Отгрузка для грузовика {truck} уже прошла')
            return HttpResponseRedirect(reverse('truck_list'))

        shipment_log = use_cases.ShipCargoFromTruck(
            truck=truck,
            x_coord=form.cleaned_data['x_coord'],
            y_coord=form.cleaned_data['y_coord']
        ).run()

        return self.render_to_response({
            'truck': truck,
            'shipment_log': shipment_log,
        })
