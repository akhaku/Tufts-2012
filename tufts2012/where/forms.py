from django import forms
from django.forms import ValidationError
from util.forms import UtilModelForm
from where.models import Location

class LocationForm(UtilModelForm):
    """ The class for a form to put in a user's location
    """
    class Meta:
        model = Location
        fields = ('name',)

    first_name = forms.CharField(max_length=20, required=True,
            help_text="First Name")
    last_name = forms.CharField(max_length=30, required=True,
            help_text="Last Name")
