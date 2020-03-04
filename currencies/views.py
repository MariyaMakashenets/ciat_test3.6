# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Currencies, CurrenciesHistory
from .forms import CurrenciesHistoryForm


def all_currencies(request):
    all_curr = Currencies.objects.all()
    list_last_curr = []
    for curr in all_curr:
        last_curr = CurrenciesHistory.objects.filter(period__lte=datetime.today(), curr_id = curr.id).values('curr', 'buying_rate',                                                                                   'selling_rate').latest('period')
        list_last_curr.append({'curr': curr.short_name, 'curr_id': curr.id,'buying_rate': last_curr['buying_rate'], 'selling_rate': last_curr['selling_rate'], })

    context = {
        'ondate': datetime.today().strftime("%d/%m/%y"),
        'last_curr': list_last_curr,
    }
    return render(request, 'currencies/all_curr.html', context)

def currency_history(request,id):
    last_curr_inf = []
    curr = Currencies.objects.filter(id=id)[0]
    last_curr = CurrenciesHistory.objects.filter(period__lte=datetime.today(), curr_id=id).values('curr',
                                                                                                  'buying_rate',
                                                                                                  'selling_rate').latest(
        'period')
    last_curr_inf.append({'curr': curr.short_name, 'curr_id': curr.id, 'buying_rate': last_curr['buying_rate'],
                          'selling_rate': last_curr['selling_rate'], })
    curr_history = CurrenciesHistory.objects.filter(curr_id = id).order_by('period')
    context = {
        'curr_id': id,
        'curr': f'{curr.name}({curr.short_name})',
        'last_curr': last_curr_inf,
        'curr_history': curr_history,
    }
    return render(request, 'currencies/history_curr.html', context)

def currency_history_by_period(request,id):
    _datefrom = request.GET.get('datefrom')
    _dateto = request.GET.get('dateto')
    curr = Currencies.objects.filter(id=id)[0]
    curr_history = CurrenciesHistory.objects.filter(curr_id = id).order_by('period')
    errors =[]
    if _datefrom=='':
        errors.append('Необходимо заполнить дату начала')
    if _dateto=='':
        errors.append('Необходимо заполнить дату конца')
    curr_table = []
    if not len(errors):
        datefrom = datetime.strptime(_datefrom, "%Y-%m-%d")
        dateto = datetime.strptime(_dateto, "%Y-%m-%d")
        if datefrom > dateto:
            errors.append('Дата начала не может быть больше даты конца')
        else:
            ondate = datefrom
            while ondate <= dateto:
                curr_table.append({'period':ondate.strftime("%Y-%m-%d"),'curr':''})
                ondate+=timedelta(days=1)

            qs_changes_in_period = CurrenciesHistory.objects.filter(period__gte=datefrom, period__lte=dateto, curr_id=id).order_by('period')
            curr=''
            buying_rate=''
            selling_rate=''
            for row in qs_changes_in_period:
                for row1 in curr_table:
                    if str(row.period) == row1['period']:
                        row1['curr']=row.curr
                        row1['buying_rate']=row.buying_rate
                        row1['selling_rate'] = row.selling_rate
                        curr=row.curr
                        buying_rate=row.buying_rate
                        selling_rate=row.selling_rate
                    elif row.period<datetime.strptime(row1['period'],"%Y-%m-%d").date():
                        row1['curr'] = curr
                        row1['buying_rate'] = buying_rate
                        row1['selling_rate'] = selling_rate

            if curr_table[0]['curr']=='':
                try:
                    last_curr_before_period = CurrenciesHistory.objects.filter(period__lt=datefrom, curr_id=id).latest('period')
                    j = 0
                    while curr_table[j]['curr'] == '':
                        curr_table[j]['curr'] = last_curr_before_period.curr
                        curr_table[j]['buying_rate'] = last_curr_before_period.buying_rate
                        curr_table[j]['selling_rate'] = last_curr_before_period.selling_rate
                        j += 1
                except:
                    ''
    context = {
        'curr_id': id,
        'curr': f'{curr.name}({curr.short_name})',
        'datefrom': _datefrom,
        'dateto':_dateto,
        'curr_table': curr_table,
        'errors':errors,
        'curr_history': curr_history,
    }
    return render(request, 'currencies/history_curr_by_period.html', context)

class CurrencyHistoryCreateView(CreateView):
    model = CurrenciesHistory
    form_class = CurrenciesHistoryForm
    template_name = 'currencies/history_curr_add.html'

    def get_success_url(self):
        return f'/currencies/currency_history/{self.object.curr_id}'

    def get_initial(self):
        initial_data = super(CurrencyHistoryCreateView, self).get_initial()
        initial_data['curr_id'] = self.kwargs['id']
        return initial_data

class CurrencyHistoryDeleteView(DeleteView):
    model = CurrenciesHistory
    success_url = '/currencies/'

    def get(self, request, *args, **kwargs):
        return self.post( request, *args, **kwargs)

    def get_success_url(self):
        return f'/currencies/currency_history/{self.object.curr_id}'



