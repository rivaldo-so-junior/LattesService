# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from scriptLattes.grupo import *
from scriptLattes.util import *
from lattes_service.settings import ARQUIVO_DE_CONFIGURACAO_SCRIPT_LATTES, COMPILAR_PRODUCAO
from .models import *
from datetime import datetime
from django.apps import apps

logger = logging.getLogger(__name__)

class PersisteDadosDosCurriculosLattes:
    def __init__(self, arquivo_de_configuracao_script_lattes):
        try:
            self.grupo = Grupo(arquivo_de_configuracao_script_lattes)
        except:
            logger.error(u"Erro ao iniciar o scriptLattes. "
                         u"Verifique se o arquivo scriptLattes/scriptLattes.config esta devidamente configurado.",
                         exc_info=True)
            raise

        try:
            print u"--- Iniciando o download e processando os dados dos Curriculos Lattes - {}.".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            self.grupo.carregarDadosCVLattes()  # obrigatorio
        except:
            logger.error(u"Erro ao processar os dados do scriptLattes. "
                         u"Verifique se o arquivo de configuracao esta devidademente configurado.",
                         exc_info=True)
            raise

        if COMPILAR_PRODUCAO:
            try:
                print u"--- Compilando os dados dos {} curriculos baixados - {}.".format(len(self.grupo.listaDeMembros), datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                self.grupo.compilarListasDeItems()  # obrigatorio
            except:
                logger.error(u"Erro ao compilar os dados do scriptLattes. "
                             u"Verifique o arquivo de log para maiores informacoes.",
                             exc_info=True)
                raise


    def limpar_tabelas(self):
        # from django.core.management.color import no_style
        from django.db import connection

        print u"--- Limpando as tabelas do banco de dados do sistema - {}.".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        try:
            ### Muito lento para muitos registros, pois o Django itera cada registro.
            ### A melhor saida e truncar as tabelas.
            # Producao.objects.all().delete()
            # Membro.objects.all().delete()
            #
            # with connection.cursor() as cursor:
            #     sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Membro, Producao, ProducaoMembro])
            #     for sql in sequence_sql:
            #         cursor.execute(sql)

            ### Nao e recomendavel executar SQL puro, o ideal e utilizar os metodos do ORM para manter
            ### a compatibilidade com diversos SGBDs, mas neste caso a melhor alternativa foi ignorar
            ### a recomendacao porque nao foi encontrada outra forma de se TRUNCAR as tabelas.
            with connection.cursor() as cursor:
                cursor.execute('TRUNCATE TABLE {} RESTART IDENTITY CASCADE'.format(Producao._meta.db_table))
                cursor.execute('TRUNCATE TABLE {} RESTART IDENTITY CASCADE'.format(Membro._meta.db_table))
        except:
            logger.error(u"Erro ao limpar as tabelas. "
                         u"Execute a operacao diretamente no banco de dados e execute o sistema novamente.",
                         exc_info=True)
            raise

    def persistir_membros(self):
        print u"--- Iniciando a persistencia dos dados no banco de dados - {}.".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print u"------ Persistindo a lista de orientadores - {}.".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        for membro in self.grupo.listaDeMembros:
            print u"--------- Persistindo os dados de identificacao do(a) orientador(a) {} - {}.".format(membro.nomeCompleto, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            try:
                Membro.objects.create(
                    id_membro=membro.idMembro,
                    id_lattes=membro.idLattes,
                    nome_inicial=membro.nomeInicial,
                    nome_lattes=membro.nomeCompleto
                )
            except:
                logger.info(u"Nao foi possivel incluir o pesquisador {}, "
                            u"ID Lattes: {}.".format(membro.nomeInicial, membro.idLattes),
                            exc_info=True)

    def persistir_producao_compilada(self):
        ''' Varre todos os Models do app curriculo,
            obtem os objetos do scriptLattes que contem dados de producao cientifica,
            itera sobre os objetos obtidos,
            varre a lista de campos do Model que esta sendo iterado a fim de
            obter os dados do objeto do scriptLattes,
            salva os dados do Model no banco de dados'''

        print u"------ Persistindo a producao dos {} orientadores - {}.".format(len(self.grupo.listaDeMembros),datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        app_name = __name__.split('.', 1)[0]
        app_models = apps.get_app_config(app_name).get_models()
        for model in app_models:
            model_name = model.__name__
            if (model_name not in ('Extracao', 'Membro', 'Producao', 'ProducaoMembro')):
                listaDeProducao = getattr(self.grupo.compilador, "listaCompleta" + model_name)
                if (len(listaDeProducao)):
                    total = sum(len(nestedDict) for nestedDict in listaDeProducao.itervalues())
                    print u"--------- Persistindo {} {} - {}.".format(total, model._meta.verbose_name_plural, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                    for ano in listaDeProducao:
                        for producao in listaDeProducao[ano]:
                            try:
                                membros = Membro.objects.filter(id_membro__in=producao.idMembro)
                                dados = {}
                                for field in model._meta.fields:
                                    field_name = field.name
                                    if field_name not in ['id', 'producao_ptr', 'membro']:
                                        dados[r"{}".format(field_name)] = producao.__dict__[field_name]
                                instancia = model.objects.create(**dados)
                                instancia.membros = membros
                            except:
                                logger.info(r"Não foi possível incluir a producao {}, "
                                            "presente no(s) curriculo(s) do(s) "
                                            "pesquisador(es) {}".format(producao['titulo'], producao['autores']),
                                            exc_info=True)
                else:
                    print u"--------- Nao ha {} para persistir - {}.".format(model._meta.verbose_name_plural, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


    def persistir_producao_individual(self):
        ''' Percorre a lista de membros
            Percorre todos os Models do app curriculo,
            obtem os objetos do scriptLattes que contem dados de producao cientifica de cada membro,
            itera sobre os objetos obtidos,
            varre a lista de campos do Model que esta sendo iterado a fim de
                    obter os dados do objeto do scriptLattes,
            salva os dados do Model no banco de dados
            exibe os totais de producao no log'''

        print u"------ Persistindo a producao dos {} orientadores - {}.".format(len(self.grupo.listaDeMembros), datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        totais_de_producao = dict()
        app_name = __name__.split('.', 1)[0]

        for membro in self.grupo.listaDeMembros:
            print u"--------- Persistindo a producao do(a) orientador(a) {} - {}.".format(membro.nomeCompleto,
                                                                                          datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            app_models = apps.get_app_config(app_name).get_models()
            for model in app_models:
                model_name = model.__name__
                if model_name not in ('Extracao', 'Membro', 'Producao', 'ProducaoMembro'):
                    listaDeProducao = getattr(membro, "lista" + model_name)
                    total = len(listaDeProducao)
                    if total:
                        ### a ideia dessa soma e mostrar o que foi realmente importado do Lattes
                        ### para poder comparar com o que foi persistido caso algum problema tenha ocorrido.
                        key = model._meta.verbose_name_plural
                        if key in totais_de_producao:
                            totais_de_producao[key] += total
                        else:
                            totais_de_producao[key] = total
                        print u"------------ Persistindo {} {} - {}.".format(total, model._meta.verbose_name_plural,
                                                                             datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                        for producao in listaDeProducao:
                            try:
                                membros = Membro.objects.filter(id_membro=membro.idMembro)
                                dados = {}
                                for field in model._meta.fields:
                                    field_name = field.name
                                    if field_name not in ['id', 'producao_ptr', 'membro']:
                                        dados[r"{}".format(field_name)] = producao.__dict__[field_name]
                                instancia = model.objects.create(**dados)
                                instancia.membros = membros
                            except:
                                logger.info(u"Nao foi possível incluir a producao {}, "
                                            u"presente no curriculo do "
                                            u"pesquisador {}".format(producao['titulo'], membro.nomeCompleto),
                                            exc_info=True)

        for tipo,total in totais_de_producao.items():
            print u"------ Foram persistidos(as) {} {} - {}.".format(total, tipo, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


    def persistir(self):
        self.limpar_tabelas()
        self.persistir_membros()

        if COMPILAR_PRODUCAO:
            self.persistir_producao_compilada()
        else:
            self.persistir_producao_individual()


def persistir_job():
    print u'----------------------------------------------------------'
    print u'Inicio do job - {}.'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print u'----------------------------------------------------------'

    persiste = PersisteDadosDosCurriculosLattes(ARQUIVO_DE_CONFIGURACAO_SCRIPT_LATTES)

    persiste.persistir()
    del persiste
    Extracao.objects.create()

    print u'----------------------------------------------------------'
    print u'Fim do job - {}.'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print u'----------------------------------------------------------'
