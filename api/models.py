# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class UltimaRequisicao(models.Model):
    full_path = models.TextField() #Endpoint + Path Params + Query Params
    data = models.DateTimeField(auto_now_add=True) # Data da requisição
    ip = models.CharField(max_length=255) # IP do requisitante
    http_host = models.TextField() # Host name do requisitante
