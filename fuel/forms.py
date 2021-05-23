# **************************************************************
# START dongilay
# **************************************************************
from django import forms
from dal import autocomplete
from .models import Transaction, Tank, Reading
from workforce.models import BasicProfile, ProjectSite
from fleet.models import UnitProfile

class TransactionForm(forms.ModelForm):
    processed_by = forms.ModelChoiceField(
        queryset=BasicProfile.objects.all(),
        widget=autocomplete.ModelSelect2(url='workforce:basic_profiles')
    )

    tank_site = forms.ModelChoiceField(
        queryset=Tank.objects.all(),
        widget=autocomplete.ModelSelect2(url='fuel:tanks')
    )

    project_site = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site')
    )

    unit = forms.ModelChoiceField(
        queryset=UnitProfile.objects.all(),
        widget=autocomplete.ModelSelect2(url='fleet:units')
    )

    class Meta:
        model = Transaction
        fields = ('__all__')

class ReadingForm(forms.ModelForm):
    tank = forms.ModelChoiceField(
        queryset=Tank.objects.all(),
        widget=autocomplete.ModelSelect2(url='fuel:tanks')
    )

    conducted_by = forms.ModelChoiceField(
        queryset=BasicProfile.objects.all(),
        widget=autocomplete.ModelSelect2(url='workforce:basic_profiles')
    )

    class Meta:
        model = Reading
        fields = ('__all__')

class TankForm(forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site')
    )

    class Meta:
        model = Tank
        fields = ('__all__')



# **************************************************************
# END dongilay
# **************************************************************