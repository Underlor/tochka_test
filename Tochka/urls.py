"""Tochka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from parse_app.views import ParserView
from web.views import IndexView, ShareView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(
        [
            url(r'^$', IndexView.as_view(api=True)),
            url(r'^(?P<share_name>[\d\w]+)/$', ShareView.as_view(api=True)),
        ]
    )),
    url(r'^parse/$', ParserView.as_view(template_name='parse/index.html'), name='parse'),
    url(r'^(?P<share_name>[\d\w]+)/$', ShareView.as_view(template_name='web/index.html')),
    url(r'^$', IndexView.as_view(template_name='web/index.html'), name='index'),
]

