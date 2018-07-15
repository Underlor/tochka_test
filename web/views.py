import json
from datetime import datetime

from django import forms
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView, FormView

from parse_app.models import Share, Trader


class MainView(TemplateView):
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class IndexView(MainView):
    def get(self, request, *args, **kwargs):
        kwargs['shares'] = Share.objects.order_by().values('name').distinct()
        return super().get(request, *args, **kwargs)


class ShareView(MainView):
    def get(self, request, *args, **kwargs):
        kwargs['shares'] = Share.objects.filter(name=kwargs['share_name'])
        kwargs['share_name'] = kwargs['shares'].first().name
        return super().get(request, *args, **kwargs)


class TradersView(ShareView):
    def get(self, request, *args, **kwargs):
        kwargs['traders'] = Trader.objects.filter(share=kwargs['share_name'])

        if 'trader_id' in kwargs:
            kwargs['traders'] = kwargs['traders'].filter(name=Trader.objects.filter(
                id=kwargs['trader_id']).first().name)

        return super().get(request, *args, **kwargs)


class AnaliticsView(ShareView):
    def get(self, request, *args, **kwargs):
        if 'date_from' in request.GET and 'date_to' in request.GET:
            try:
                date_from = datetime.strptime(request.GET['date_from'], "%m/%d/%Y")
                date_to = datetime.strptime(request.GET['date_to'], "%m/%d/%Y")

                shares = Share.objects.filter(name=kwargs['share_name']).filter(
                    Q(date=date_from) | Q(date=date_to)).all()

                if shares.count() < 2:
                    kwargs['error'] = 'Не удалось посчитать разницу цен. Не удалось найти все акции по указанным датам.'
                    return super().get(request, *args, **kwargs)

                kwargs['prices'] = {
                    'open': shares[0].open - shares[1].open,
                    'close': shares[0].close - shares[1].close,
                    'higt': shares[0].higt - shares[1].higt,
                    'low': shares[0].low - shares[1].low,
                }

            except ValueError:
                kwargs['error'] = 'Ошибка в формате данных для даты. Формат: Месяц/День/Год'
                return super().get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)
