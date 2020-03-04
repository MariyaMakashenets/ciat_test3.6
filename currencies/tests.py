from django.test import TestCase
from .models import *


class TestCurr(TestCase):

    def setUp(self):
        self.curr_a = Currencies.objects.create(name='Test', short_name='T')
        self

    def create_on_today(self):
        curr_h3 = CurrenciesHistory(curr=self.curr_a, period=date.today(), buying_rate=1.2, selling_rate=2.2)
        curr_h3.save()
        self.assertTrue(isinstance(curr_h3, CurrenciesHistory))
        self.assertEqual(curr_h3.__str__(), f'{str(date.today())}/{str(self.curr_a.short_name)}/{str(1.2) }/{str(2.2)}')

    def create_on_any_day(self):
        curr_h1 = CurrenciesHistory(curr=self.curr_a, period=date(year=2020, month=1, day=1), buying_rate=1,
                                    selling_rate=2)
        curr_h1.save()
        self.assertTrue(isinstance(curr_h1, CurrenciesHistory))
        self.assertEqual(curr_h1.__str__(), f'{str(date(year=2020, month=1, day=1))}/{str(self.curr_a.short_name)}/{str(1)}/{str(2)}')

    def delete_curr(self):
        curr_h2 = CurrenciesHistory(curr=self.curr_a, period=date(year=2020, month=1, day=3), buying_rate=1.1,
                                    selling_rate=2.1)
        curr_h2.save()
        curr_h2.delete()
        self.assertFalse(CurrenciesHistory.objects.filter(pk=self.curr_h2.pk).exists())

