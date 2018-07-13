from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class ParserView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(ParserView, self).get_context_data(**kwargs)

        return context

    def post(self, request, *args, **kwargs):
        return HttpResponse('')
