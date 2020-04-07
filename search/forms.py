from django import forms
from django.forms import ModelMultipleChoiceField
#from uploads.core.models import Document
from users.models import CustomUser, Bibgroup

from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit



class DevkeyForm(forms.Form):
    inputDevKey = forms.CharField(label="ADS API Token", max_length=250,required=False)

    class Meta:
        model = CustomUser
        fields = ('devkey',)