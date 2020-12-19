# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from cron import gerar_arquivo_list_job


### apenas para fins de teste e debug no ambiente de desenvolvimento
def gerar_arquivo_list(request):
    gerar_arquivo_list_job()
    return HttpResponse("Processado")

