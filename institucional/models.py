# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Programa(models.Model):
    cod_capes = models.CharField(max_length=20, primary_key=True)
    nome = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = "Programas"
        managed = False
        db_table = 'programas'

class Orientador(models.Model):
    cod_lattes_16 = models.CharField(max_length=16, primary_key=True)
    nome = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = "Orientadores"
        managed = False
        db_table = 'orientadores'

class ProgramaOrientador(models.Model):
    cod_capes = models.ForeignKey(Programa)
    cod_lattes_16 = models.ForeignKey(Orientador)
    class Meta:
        verbose_name_plural = "Programas/Orientadores"
        managed = False
        db_table = 'programas_orientadores'
