
from django.conf.urls import url, include
from rest_framework import routers, schemas, documentation

from api.services import *

router = routers.DefaultRouter()
router.register(r'orientador', ProducaoPorMembroViewSet)
# router.register(r'producao_por_tipo/(?P<tipo>)/?$', ProducaoPorTipoViewSet)

schema_view = schemas.get_schema_view(title='LattesService API',
                                      description='Esta API fornece dados de um determinado orientador '
                                                  'a partir da extracao realizada do Curriculo Lattes '
                                                  'com o uso do scriptLattes.'
                                      )

docs = documentation.include_docs_urls(title='LattesService API',
                                       description='Esta API fornece dados de um determinado orientador '
                                                   'a partir da extracao realizada do Curriculo Lattes '
                                                   'com o uso do scriptLattes.'
                                       )

urlpatterns = [
    url(r'^api/producao/', include(router.urls)),
    url(r'^api/producao/producao_por_tipo/(?P<tipo>[\w\_]+)/(?P<id_lattes>[0-9]{16})/?$', ProducaoPorTipoViewSet.as_view({'get':'list'}) ),
    url(r'^schema/', schema_view),
    url(r'^docs/', docs),
]
