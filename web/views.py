import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from parse_app.models import Share


class ApiBasedView(TemplateView):
    api = False

    def return_data(self, request, *args, **kwargs):
        if self.api:
            return HttpResponse(json.dumps(**kwargs))
        return super().get(request, *args, **kwargs)


class IndexView(ApiBasedView):
    def get(self, request, *args, **kwargs):
        kwargs['shares'] = Share.objects.all()
        return self.return_data(request, *args, **kwargs)


class ShareView(ApiBasedView):
    def get(self, request, *args, **kwargs):
        try:
            kwargs['share'] = Share.objects.get(name=kwargs['share_name'])
        except Share.DoesNotExist:
                return redirect('/')
        return self.return_data(request, *args, **kwargs)
