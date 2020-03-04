from django import forms
from .models import CurrenciesHistory

class CurrenciesHistoryForm(forms.ModelForm):

    class Meta(object):
        model = CurrenciesHistory
        fields = ('curr', 'period', 'buying_rate', 'selling_rate',)

