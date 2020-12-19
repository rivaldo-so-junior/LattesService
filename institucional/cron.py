# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv, codecs, cStringIO, logging
from lattes_service.settings import LISTA_DE_ORIENTADORES_SCRIPT_LATTES
from institucional.models import Orientador
from datetime import datetime

logger = logging.getLogger(__name__)

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    fonte: https://docs.python.org/2/library/csv.html
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            try:
                self.writerow(row)
            except:
                logger.info(u"Não foi possível incluir o orientador {} no arquivo.".format(row),
                            exc_info=True)


def gerar_arquivo_list_job():
    print u'###################'
    print u'Inicio do job - {}.'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print u'---------- Buscando lista de orientadores no banco.'
    orientadores = Orientador.objects.all().using('institucional').order_by('nome').values_list()
    print u'---------- {} orientadores encontrados.'.format(len(orientadores))
    path = LISTA_DE_ORIENTADORES_SCRIPT_LATTES

    try:
        print u'---------- Abrindo o arquivo para escrita.'
        writer = UnicodeWriter(open(path, "wb"))
    except:
        logger.error(u"Não foi possível encontrar o arquivo {}.".format(path),
                    exc_info=True)
        raise

    print u'---------- Iniciando a escrita no arquivo.'
    writer.writerows(orientadores)
    print u'---------- Fim da escrita no arquivo.'

    del writer

    print u'Fim do job - {}.'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print u'###################'
