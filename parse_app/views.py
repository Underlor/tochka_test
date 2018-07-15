import re
import time
from threading import Thread

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django import forms

# Create your views here.
from django.views.generic import FormView
from multiprocessing.dummy import Pool

from parse_app.models import Share, Trader


class Parser(Thread):
    threads_count = 1
    name_list = []

    def __init__(self, threads, names):
        self.name_list = names.split(',')
        self.threads_count = int(threads)
        super(Parser, self).__init__()

    @staticmethod
    def save_data(source, share):
        table = source.find('table', {'class': 'certain-width'})
        rows = table.find_all('tr')
        items = []
        for row in rows:
            cols = [ele.text.strip() for ele in row.find_all('td')]
            if len(cols) > 0:
                items.append(Trader(
                    share=share,
                    name=cols[0],
                    relation=cols[1],
                    lastdate=(datetime.strptime(cols[2], "%m/%d/%Y")),
                    transaction_type=cols[3],
                    owner_type=cols[4],
                    shares_traded=cols[5].replace(',', ''),
                    last_price=cols[6].replace(',', '') if cols[6].replace(',', '') else 0,
                    shares_held=cols[7].replace(',', ''),
                ))

        Trader.objects.bulk_create(items)

    @staticmethod
    def parce(share):
        time_start = datetime.now()
        share = share.strip()
        page = requests.get(f'http://www.nasdaq.com/symbol/{share}/historical')
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find('table').parent.find_next_siblings()[3].find('tbody')
        rows = table.find_all('tr')
        counter = 0
        items = []
        for row in rows:
            cols = [ele.text.strip() for ele in row.find_all('td')]
            if not len(cols[1]):
                continue
            print(datetime.strptime(cols[0], "%m/%d/%Y"))
            items.append(Share.objects.create(
                name=share,
                date=(datetime.strptime(cols[0], "%m/%d/%Y")),
                open=cols[1].replace(',', ''),
                higt=cols[2].replace(',', ''),
                low=cols[3].replace(',', ''),
                close=cols[4].replace(',', ''),
                volume=cols[5].replace(',', ''),
            ))
            counter += 1
        # Share.objects.bulk_create(items)
        time_start2 = datetime.now()

        page = requests.get(f'https://www.nasdaq.com/symbol/{share}/insider-trades')
        soup = BeautifulSoup(page.text, 'html.parser')
        paginator = soup.find('a', {'id': 'quotes_content_left_lb_LastPage'})
        Parser.save_data(soup, share)
        if paginator:
            print(paginator['href'])
            res = re.search(r'page=(\d+)', paginator['href'])
            if res:
                page = int(res.group(1))
                pages = 10 if page > 10 else page
                for i in range(1, pages + 1):
                    print(share, i)
                    page = requests.get(f'https://www.nasdaq.com/symbol/{share}/insider-trades?page={i}')
                    soup = BeautifulSoup(page.text, 'html.parser')
                    Parser.save_data(soup, share)
        return {
            'time to shera parse': (time_start2 - time_start).seconds,
            'ti me to traders parse': (datetime.now() - time_start2).seconds,
        }

    def start(self):
        pool = Pool(self.threads_count)
        results = pool.map(self.parce, self.name_list)
        print(results)


class InputForm(forms.Form):
    thread_count = forms.IntegerField()
    file = forms.FileField()


class ParserView(FormView):
    form_class = InputForm

    def post(self, request, *args, **kwargs):
        form = InputForm(request.POST, request.FILES)
        if form.is_valid():
            file_data = request.FILES['file'].read().decode("utf-8")
            time_start = datetime.now()
            Share.objects.all().delete()
            Trader.objects.all().delete()
            Parser(request.POST['thread_count'], file_data).start()
            print('Fulltime:', (datetime.now() - time_start).seconds)
        return self.get(request, *args, **kwargs)
