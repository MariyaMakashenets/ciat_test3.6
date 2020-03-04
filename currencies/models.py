# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import date

class Currencies(models.Model):

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Наименование валюты'
    )
    short_name = models.CharField(
        max_length=4,
        blank=False,
        unique=True,
        verbose_name='Краткое наименование'
    )

    def __str__(self):
        return self.name


class CurrenciesHistory(models.Model):

    class Meta:
        verbose_name = 'Курс валюты'
        verbose_name_plural = 'Курсы валют'
        ordering = ['period']

    curr = models.ForeignKey(
        Currencies,
        on_delete=models.PROTECT,
        verbose_name='Валюта',
    )
    period = models.DateField(default=date.today, verbose_name='Дата')
    buying_rate = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Курс покупки')
    selling_rate = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Курс продажи')

    def __str__(self):
        return f'{str(self.period)}/{str(self.curr.short_name)}/{str(self.buying_rate) }/{str(self.selling_rate)}'


