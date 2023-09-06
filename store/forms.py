from django import forms
from .models import ReviewRating
from django.contrib import messages

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
        # Agrega la validación del rating como obligatorio
        widgets = {
            'rating': forms.RadioSelect(attrs={'required': 'required'})
        }

    