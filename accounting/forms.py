from django import forms
from dal import autocomplete

from django.contrib.auth.models import User

from accounting.models import (Item, ItemCode, OrderRequest, PriceList, CashBudget,
            Liquidation, Supplier, Entry, FundRequest, SubconBilling)
from workforce.models import ProjectSite, Subcon


class FundRequestForm(forms.ModelForm):
    request_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:matic')
    )
    project_site = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site')
    )

    class Meta:
        model = FundRequest
        fields = ('__all__')


class EntryForm(forms.ModelForm):
    transaction_by = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:matic'),
        required=False
    )
    project_site = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site')
    )
    base_por = forms.ModelChoiceField(
        queryset=OrderRequest.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:purchase'),
        required=False
    )
    item = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:item_name'),
        required=False
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:supplier'),
        required=False
    )
    subcon = forms.ModelChoiceField(
        queryset=Subcon.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:subcon'),
        required=False
    )
    account_code = forms.ModelChoiceField(
        queryset=ItemCode.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:code'),
        required=False
    )

    class Meta:
        model = Entry
        fields = ('__all__')

class EntryForm2(forms.ModelForm):
    transaction_by = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:matic'),
        required=False
    )
    project_site = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site')
    )
    item = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:item_name'),
        required=False
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:supplier'),
        required=False
    )
    subcon = forms.ModelChoiceField(
        queryset=Subcon.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:subcon'),
        required=False
    )
    account_code = forms.ModelChoiceField(
        queryset=ItemCode.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:code'),
        required=False
    )

    class Meta:
        model = Entry
        fields = ('__all__')


class OrderRequestForm(forms.ModelForm):
    request_by = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:matic'),
        required=False
    )
    project_site = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site')
    )
    item = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:item_name')
    )
    purchaser = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:matic'),
        required=False
    )

    class Meta:
        model = OrderRequest
        fields = ('__all__')


class SubconBillingForm(forms.ModelForm):
    request_by = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:matic')
    )
    project_site = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site')
    )
    subcon = forms.ModelChoiceField(
        queryset=Subcon.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:subcon')
    )

    class Meta:
        model = SubconBilling
        fields = ('__all__')


#Old data
class CashBudgetForm(forms.ModelForm):
    issued_by = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:matic')
    )
    issued_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:matic')
    )

    class Meta:
        model = CashBudget
        fields = ('__all__')


class LiquidationForm(forms.ModelForm):
    base_budget = forms.ModelChoiceField(
        queryset=CashBudget.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:cash')
    )
    base_por = forms.ModelChoiceField(
        queryset=OrderRequest.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:purchase'),
        required=False
    )
    project_site = forms.ModelChoiceField(
        queryset=ProjectSite.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:project_site')
    )
    issued_by = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:matic')
    )
    item = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:item_name'),
        required=False
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        widget=autocomplete.ModelSelect2(url='accounting:supplier'),
        required=False
    )


    class Meta:
        model = Liquidation
        fields = ('__all__')


# **************************************************************
# START dongilay
# **************************************************************

class SupplierForm(forms.ModelForm):

    address = forms.CharField(max_length=200, widget=forms.Textarea)

    class Meta:
        model = Supplier
        fields = ('__all__')

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('__all__')

# **************************************************************
# END dongilay
# **************************************************************
