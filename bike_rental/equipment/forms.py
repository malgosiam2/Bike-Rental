from django import forms

class EquipmentFilterForm(forms.Form):
    SORT_CHOICES = [
        ('price_asc', 'Price: Low to High'),
        ('price_desc', 'Price: High to Low'),
        ('az_asc', 'Alphabetically'),
        ('az_desc', 'Reverse Alphabetically')
    ]
    
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, label="Sort by")

