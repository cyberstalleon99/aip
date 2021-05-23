from django import forms
from django.contrib.auth.models import User
from dal import autocomplete
from .models import Incoming, Outgoing
from accounting.models import Item
from workforce.models import ProjectSite, Outsider
from fleet.models import UnitProfile

class IncomingForm(forms.ModelForm):
    received_by = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:matic')
    )
    project_site = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site')
    )
    item = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:item_name')
    )

    # def __init__(self, *args, **kwargs):
    #     self.incoming_id = kwargs.pop('incoming_id')
    #     super(IncomingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Incoming
        fields = ('__all__')

class OutgoingForm(forms.ModelForm):
    project_site = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site')
    )
    released_by = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:matic'),
    )
    released_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:matic'),
        required=False
    )
    released_out = forms.ModelChoiceField(
        queryset=Outsider.objects.all(),
        widget=autocomplete.ModelSelect2(url='workforce:outsiders'),
        required=False
    )
    unit = forms.ModelChoiceField(
        queryset=UnitProfile.objects.all(),
        widget=autocomplete.ModelSelect2(url='fleet:units'),
        required=False
    )
    details = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Details here...'}))

    # def clean(self):
    #     cleaned_data = super().clean()
    #     quantity = cleaned_data.get("quantity")
    #     outgoing_id = cleaned_data.get("")



    class Meta:
        model = Outgoing
        # exclude = ('base_in',)
        fields = ('__all__')