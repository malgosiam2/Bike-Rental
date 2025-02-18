from django import forms
from .models import Order, BikeItem, AccessoryItem
from django.forms.models import inlineformset_factory
from datetime import date, timedelta

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_date', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'order_date': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}) 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['min'] = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.fields['start_date'].widget.attrs['max'] = (date.today() + timedelta(days=30)).strftime('%Y-%m-%d')
        self.fields['start_date'].widget.attrs['onchange'] = "updateEndDateLimits()"

    def clean(self):
        cleaned_data = super().clean()
        order_date = cleaned_data.get('order_date')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if order_date and start_date:
            if start_date <= order_date:
                raise forms.ValidationError('Wrong date.')
            if start_date > order_date + timedelta(days=30):
                raise forms.ValidationError('Wrong date.')
        
        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError('Wrong date.')
            if end_date > start_date + timedelta(days=14):
                raise forms.ValidationError('Wrong date.')

        return cleaned_data


class AccessoryItemForm(forms.ModelForm):
    class Meta:
        model = AccessoryItem
        fields = ['equipment', 'quantity']
        widgets = {
            'equipment': forms.Select(attrs={'class': 'accessory-field'})
        }


class BikeItemForm(forms.ModelForm):
    class Meta:
        model = BikeItem
        fields = ['equipment', 'quantity']
        widgets = {
            'equipment': forms.Select(attrs={'class': 'equipment-field'}),
        }
    

    

BikeItemFormSet = inlineformset_factory(Order, BikeItem, form=BikeItemForm, extra=4)
AccessoryItemFormSet = inlineformset_factory(Order, AccessoryItem, form=AccessoryItemForm, extra=4)

    