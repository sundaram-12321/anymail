#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.verify, name='main'),
    path('index1/', views.index, name='index'),
]
