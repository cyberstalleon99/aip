# **************************************************************
# START dongilay
# **************************************************************
from django import forms
from django.core.exceptions import ValidationError
import datetime
from dal import autocomplete
from .models import Leave, BasicProfile, Outsider, ProjectSite, FileDocument, Subcon

class LeaveForm(forms.ModelForm):
    base_profile = forms.ModelChoiceField(
        queryset=BasicProfile.objects.all(),
        widget=autocomplete.ModelSelect2(url='workforce:basic_profiles'),
    )
    reason = forms.CharField(widget=forms.Textarea)
    date_from = forms.DateField(initial=datetime.date.today)

    def clean_date_to(self):
        date_to = self.cleaned_data['date_to']
        date_from = self.cleaned_data['date_from']
        if date_to < date_from:
            raise ValidationError("Date To Field cannot be less than Date From Field!")
        return date_to

    class Meta:
        model = Leave
        fields = ('__all__')
        exclude = (
            'create_date', 'tots_days',
            'approval_super', 'approved_by_super', 'date_approved_super',
            'approval', 'approved_by', 'date_approved'
        )

class UpdateLeaveForm(forms.ModelForm):
    # date_approved_super = forms.DateField(initial=datetime.date.today, disabled=True)
    reason = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Leave
        fields = ('__all__')
        exclude = (
            'create_date', 'tots_days',
        )

class SuperLeaveForm(forms.ModelForm):
    base_profile = forms.ModelChoiceField(
        queryset=BasicProfile.objects.all(),
        widget=autocomplete.ModelSelect2(url='workforce:basic_profiles'),
    )
    reason = forms.CharField(widget=forms.Textarea)
    date_approved_super = forms.DateField(initial=datetime.date.today, disabled=True)

    def clean_approval_super(self):

        data = self.cleaned_data['approval_super']
        if data == "For Approval":
            raise ValidationError("Status is required! You can't submit with Status still For Approval!")
        return data

    class Meta:
        model = Leave
        fields = '__all__'
        exclude = ('create_date', 'approved_by_super', 'approval', 'approved_by', 'date_approved')

class AdminLeaveForm(forms.ModelForm):
    date_approved = forms.DateField(initial=datetime.date.today, disabled=True)

    def clean_approval(self):

        data = self.cleaned_data['approval']
        if data == "For Approval":
            raise ValidationError("Status is required! You can't submit with Status still For Approval!")
        return data

    class Meta:
        model = Leave
        fields = ('approval', 'date_approved', 'remarks')

class OutsiderForm(forms.ModelForm):

    class Meta:
        model = Outsider
        fields = ('__all__')

class SubconForm(forms.ModelForm):

    project_site = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site')
    )

    class Meta:
        model = Subcon
        fields = ('__all__')
        exclude = ('create_date',)

class FileDocumentForm(forms.ModelForm):

    class Meta:
        model = FileDocument
        fields = ('__all__')

# **************************************************************
# END dongilay
# **************************************************************