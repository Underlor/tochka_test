from datetime import datetime, date

from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import TemplateView

from parse_app.models import Share, Trader


class MainView(TemplateView):
    api = False

    def get(self, request, *args, **kwargs):
        if self.api:
            return JsonResponse(kwargs, safe=False)
        return super().get(request, *args, **kwargs)


class IndexView(MainView):
    def get(self, request, *args, **kwargs):
        kwargs['shares'] = list(Share.objects.all().values('name').distinct())
        return super().get(request, *args, **kwargs)


class ShareView(MainView):
    def get(self, request, *args, **kwargs):
        kwargs['shares'] = Share.objects.filter(name=kwargs['share_name'])
        kwargs['shares'] = [item.json_serialise() for item in kwargs['shares']]
        return super().get(request, *args, **kwargs)


class TradersView(MainView):
    def get(self, request, *args, **kwargs):
        kwargs['traders'] = Trader.objects.filter(share=kwargs['share_name'])

        if 'trader_id' in kwargs:
            kwargs['traders'] = kwargs['traders'].filter(name=Trader.objects.filter(
                id=kwargs['trader_id']).first().name)
        kwargs['traders'] = [item.json_serialise() for item in kwargs['traders']]
        return super().get(request, *args, **kwargs)


class AnaliticsView(MainView):

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
                    'open': abs(shares[0].open - shares[1].open),
                    'close': abs(shares[0].close - shares[1].close),
                    'higt': abs(shares[0].higt - shares[1].higt),
                    'low': abs(shares[0].low - shares[1].low),
                }

            except ValueError:
                kwargs['error'] = 'Ошибка в формате данных для даты. Формат: Месяц/День/Год'
                return super().get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)


class DeltaView(MainView):
    def get(self, request, *args, **kwargs):
        shares = Share.objects.filter(name=kwargs['share_name'], date__gte=date.today().replace(day=1)).order_by('date')
        delta = request.GET.get('value')
        val_type = request.GET.get('type')
        for item in shares.all():
            item = item.json_serialise()
            for next_item in shares.all():
                next_item = next_item.json_serialise()
                if next_item[val_type] - item[val_type] >= float(delta):
                    kwargs['result'] = f"{item['date']} - {next_item['date']}"
                    return super().get(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)
