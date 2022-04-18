from django import forms


class ShipCargoFromTruckForm(forms.Form):
    x_coord = forms.IntegerField(min_value=0, required=True)
    y_coord = forms.IntegerField(min_value=0, required=True)
