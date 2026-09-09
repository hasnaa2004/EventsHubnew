
from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'date',
            'location',
            'category',
            'status',
            'event_type',
            'city',
            'price',
            'image',
        ]

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if title and len(title.strip()) < 5:
            raise forms.ValidationError(
                'عنوان الفعالية يجب أن يحتوي على 5 أحرف على الأقل.'
            )

        return title

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise forms.ValidationError(
                'سعر الفعالية لا يمكن أن يكون سالبًا.'
            )

        return price

