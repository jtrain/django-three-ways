"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from djpjax import pjax, pjaxtend

from lists.views import (
    DashboardView, CreateNewList, DetailList
)

urlpatterns = [
    url(r'^$',
        pjaxtend()(pjax()(DashboardView.as_view())),
        name='dashboard'),
    url(r'^lists/create/$',
        pjaxtend()(pjax(follow_redirects=True)(CreateNewList.as_view())),
        name='list-create'),
    url(r'^lists/(?P<pk>\d+)/$',
        pjaxtend()(pjax()(DetailList.as_view())),
        name='list-detail'),
]
