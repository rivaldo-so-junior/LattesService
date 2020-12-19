# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from cron import persistir_job


### apenas para fins de teste e debug no ambiente de desenvolvimento
def index(request):
    persistir_job()
    return HttpResponse("Processado")
