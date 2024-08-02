#
# BHExpress: Cliente de API en Python.
# Copyright (C) BHExpress <https://www.bhexpress.cl>
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la GNU Lesser General Public License (LGPL) publicada
# por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
# o (a su elección) cualquier versión posterior de la misma.
#
# Este programa se distribuye con la esperanza de que sea útil, pero SIN
# GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
# PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
# Public License (LGPL) para obtener una información más detallada.
#
# Debería haber recibido una copia de la GNU Lesser General Public License
# (LGPL) junto a este programa. En caso contrario, consulte
# <http://www.gnu.org/licenses/lgpl.html>.
#

from .. import ApiBase
from urllib.parse import urlencode

class Boleta(ApiBase):
    '''
    Módulo que permite listar todas las BHE con filtros específicos, emitir una BHE, obtener un PDF de una BHE, enviar una BHE a un email, y anular una BHE emitida.
    
    :param str api_token: Token de autenticación del usuario. Si no se proporciona, se intentará obtener de una variable de entorno.
    :param str api_url: URL base de la API. Si no se proporciona, se usará una URL por defecto.
    :param str api_version: Versión de la API. Si no se proporciona, se usará una versión por defecto.
    :param bool api_raise_for_status: Si se debe lanzar una excepción automáticamente para respuestas de error HTTP. Por defecto es True.
    '''

    def __init__(self):
        super().__init__()

    def listar(self, periodo = None, fecha_desde = None, fecha_hasta = None, receptor_codigo = None):
        '''
        Recurso que permite obtener el listado paginado de boletas de honorarios electrónicas emitidas.

        Los parámetros de entrada son filtros para obtener boletas más específicas.

        :param str periodo: Período por el cuál consultar las boletas. Puede ser: 'AAAAMM' o 'AAAA'
        :param str fecha_desde:Fecha desde cuándo consultar las boletas. Formato: 'AAAA-MM-DD'
        :param str fecha_hasta:Fecha hasta cuándo consultar las boletas. Formato: 'AAAA-MM-DD'
        :param str receptor_codigo: Código del receptor. Generalmente es el RUT del receptor sin DV.
        :return: Respuesta JSON con el listado de boletas emitidas.
        :rtype: dict
        :exception ApiException: Arroja un error cuando las fechas de fecha_desde y fecha_hasta no son correctas, o cuando se coloca sólo una de las dos.
        '''
        url = '/bhe/boletas'
        query = {}
        if periodo is not None:
            query['periodo'] = periodo
        elif fecha_desde is not None and fecha_hasta is not None:
            query['fecha_desde'] = fecha_desde
            query['fecha_hasta'] = fecha_hasta
        if receptor_codigo is not None:
            query['receptor_codigo'] = receptor_codigo
        
        query_string = urlencode(query)

        url += '?%(query)s' % {'url': url, 'query': query_string}
        response = self.client.get(url)
        
        return response.json()
    
    def emitir(self, boleta):
        '''
        Emite una nueva Boleta de Honorarios Electrónica.

        :param dict boleta: Información detallada de la boleta a emitir.
        :return: Respuesta JSON con el encabezado y detalle de la boleta emitida.
        :rtype: dict
        '''
        response = self.client.post('/bhe/emitir', data = boleta)

        return response.json()
    
    def pdf(self, numero_bhe):    
        '''
        Obtiene el PDF de una BHE emitida.

        :param str numero_bhe: Número de la BHE registrada en BHExpress.
        :return: Contenido del PDF de la BHE.
        :rtype: bytes
        '''
        url = '/bhe/pdf/%(bhe)s' % {'bhe': numero_bhe}

        return self.client.get(url).content
    
    def email(self, numero_bhe, email):    
        '''
        Envía por correo electrónico una BHE.

        :param str numero_bhe: Número de la BHE registrada en BHExpress.
        :param str email: Correo del destinatario.
        :return: Respuesta JSON con la confirmación del envío del email.
        :rtype: dict
        '''
        url = '/bhe/email/%(bhe)s' % {'bhe': numero_bhe}
        body = {
            'destinatario': {
                'email': email
            }
        }

        response = self.client.post(url, data = body)

        return response.json()
    
    def anular(self, numero_bhe, causa):
        '''
        Anula una BHE específica.

        :param str numero_bhe: Número de la BHE registrada en BHExpress.
        :param int causa: Causa de la anulación de la BHE.
        :return: Respuesta JSON con el encabezado de la boleta anulada.
        :rtype: dict
        '''
        url = '/bhe/anular/%(bhe)s' % {'bhe': numero_bhe}
        body = {
            'causa': causa
        }

        response = self.client.post(url, data = body)

        return response.json()