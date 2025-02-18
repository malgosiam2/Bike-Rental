from django import forms
from review.models import Review
from django.utils import timezone

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'date', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your review here...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now().date()
