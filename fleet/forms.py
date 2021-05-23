# **************************************************************
# START dongilay
# **************************************************************

from django import forms
from .models import Travel, UnitProfile
from workforce.models import BasicProfile, ProjectSite

from dal import autocomplete

class TravelForm(forms.ModelForm):
    # requested_by = forms.ModelChoiceField(
    #     queryset=BasicProfile.objects.all(),
    #     widget=autocomplete.ModelSelect2(url='workforce:basic_profiles'),
    #     required=False
    # )
    base_unit = forms.ModelChoiceField(
        queryset=UnitProfile.objects.all(),
        widget=autocomplete.ModelSelect2(url='fleet:units'),
        required=False
    )
    driver = forms.ModelChoiceField(
        queryset=BasicProfile.objects.all(),
        widget=autocomplete.ModelSelect2(url='workforce:basic_profiles'),
        required=False
    )
    source = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site'),
        required=True
    )
    destination = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site'),
        required=True
    )

    class Meta:
        model = Travel
        fields = ('__all__')

class UpdateTravelForm(forms.ModelForm):
    base_unit = forms.ModelChoiceField(
        queryset=UnitProfile.objects.all(),
        widget=autocomplete.ModelSelect2(url='fleet:units'),
        required=False
    )
    driver = forms.ModelChoiceField(
        queryset=BasicProfile.objects.all(),
        widget=autocomplete.ModelSelect2(url='workforce:basic_profiles'),
        required=False
    )
    source = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site'),
        required=True
    )
    destination = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site'),
        required=True
    )

    class Meta:
        model = Travel
        fields = ('__all__')
        exclude = ('requested_by',)

# **************************************************************
# END dongilay
# **************************************************************