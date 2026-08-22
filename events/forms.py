from django import forms
from django.forms import modelformset_factory
from .models import Event


class EventSearchForm(forms.Form):
    q = forms.CharField(required=False, label='بحث')
    category = forms.CharField(required=False, label='تصنيف')
    city = forms.CharField(required=False, label='مدينة')
    sort = forms.ChoiceField(
        required=False,
        choices=(('newest', 'Newest'), ('oldest', 'Oldest'))
    )


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'date', 'location',
            'category', 'status', 'event_type', 'city', 'price'
        ]


# helper to create a formset for bulk event creation/editing
def get_event_modelformset(extra=1, queryset=None):
    return modelformset_factory(
        Event,
        form=EventForm,
        extra=extra,
        can_delete=False
    )
