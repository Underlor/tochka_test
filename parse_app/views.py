import re
from datetime import datetime
from multiprocessing.dummy import Pool

import requests
from bs4 import BeautifulSoup
from django import forms
# Create your views here.
from django.views.generic import FormView

from parse_app.models import Share, Trader


class Parser:
    threads_count = 1
    name_list = []

    def __init__(self, threads, names):
        self.name_list = names.split(',')
        self.threads_count = int(threads)

    @staticmethod
    def parse_trader(source, share):
        table = source.find('table', {'class': 'certain-width'})
        if table is not None:
            rows = table.find_all('tr')
            items = []
            for row in rows:
                cols = [ele.text.strip() for ele in row.find_all('td')]
                if len(cols) > 0:
                    if not len(cols[1]):
                        continue
                    try:
                        date = (datetime.strptime(cols[2], "%m/%d/%Y"))
                    except ValueError:
                        date = datetime.today()
                    items.append(Trader(
                        share=share,
                        name=cols[0],
                        relation=cols[1],
                        lastdate=date,
                        transaction_type=cols[3],
                        owner_type=cols[4],
                        shares_traded=cols[5].replace(',', ''),
                        last_price=cols[6].replace(',', '') if cols[6].replace(',', '') else 0,
                        shares_held=cols[7].replace(',', ''),
                    ))

            Trader.objects.bulk_create(items)

    @staticmethod
    def parce_shares(session, share):
        page = session.get(f'http://www.nasdaq.com/symbol/{share}/historical')
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find('table').parent.find_next_siblings()[3].find('tbody')
        rows = table.find_all('tr')
        counter = 0
        items = []
        for row in rows:
            cols = [ele.text.strip() for ele in row.find_all('td')]
            if not len(cols[1]):
                continue
            try:
                date = (datetime.strptime(cols[0], "%m/%d/%Y"))
            except ValueError:
                date = datetime.today()
            items.append(Share(
                name=share,
                date=date,
                open=cols[1].replace(',', ''),
                higt=cols[2].replace(',', ''),
                low=cols[3].replace(',', ''),
                close=cols[4].replace(',', ''),
                volume=cols[5].replace(',', ''),
            ))
            counter += 1
        Share.objects.bulk_create(items)

    @staticmethod
    def parce_traders_pages(session, share):
        page = session.get(f'https://www.nasdaq.com/symbol/{share}/insider-trades')
        soup = BeautifulSoup(page.text, 'html.parser')
        paginator = soup.find('a', {'id': 'quotes_content_left_lb_LastPage'})
        Parser.parse_trader(soup, share)
        if paginator:
            res = re.search(r'page=(\d+)', paginator['href'])
            if res:
                page = int(res.group(1))
                pages = 10 if page > 10 else page
                for i in range(1, pages + 1):
                    page = session.get(f'https://www.nasdaq.com/symbol/{share}/insider-trades?page={i}')
                    soup = BeautifulSoup(page.text, 'html.parser')
                    Parser.parse_trader(soup, share)

    @staticmethod
    def parce_all_data(share):
        share = share.strip()
        session = requests.Session()
        Parser.parce_shares(session, share)
        Parser.parce_traders_pages(session, share)

    def start(self):
        pool = Pool(self.threads_count)
        results = pool.map(self.parce_all_data, self.name_list)
        return results


class InputForm(forms.Form):
    thread_count = forms.IntegerField()
    file = forms.FileField()


class ParserView(FormView):
    form_class = InputForm

    def post(self, request, *args, **kwargs):
        form = InputForm(request.POST, request.FILES)
        if form.is_valid():
            file_data = request.FILES['file'].read().decode("utf-8")
            Share.objects.all().delete()
            Trader.objects.all().delete()
            Parser(request.POST['thread_count'], file_data).start()
        return self.get(request, *args, **kwargs)
