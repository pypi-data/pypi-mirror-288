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

from os import getenv
import time
import requests
import urllib
import json
from abc import ABC

class ApiClient:
    '''
    Cliente para interactuar con la API de BHExpress.

    :param str token: Token de autenticación del usuario. Si no se proporciona, se intentará obtener de una variable de entorno.
    :param str url: URL base de la API. Si no se proporciona, se usará una URL por defecto.
    :param str version: Versión de la API. Si no se proporciona, se usará una versión por defecto.
    :param bool raise_for_status: Si se debe lanzar una excepción automáticamente para respuestas de error HTTP. Por defecto es True.
    '''

    __DEFAULT_URL = 'https://bhexpress.cl'
    __DEFAULT_VERSION = 'v1'

    def __init__(self, token = None, url = None, version = None, raise_for_status = True):
        '''
        Constructor para inicializar el Cliente de la API de BHExpress.
        '''
        self.token = self.__validate_token(token)
        self.url = self.__validate_url(url)
        self.rut = self.__validate_rut()
        self.headers = self.__generate_headers()
        self.version = version or self.__DEFAULT_VERSION
        self.raise_for_status = raise_for_status

    def __validate_token(self, token):
        '''
        Valida y retorna el token de autenticación.

        :param str token: Token de autenticación a validar.
        :return: Token validado.
        :rtype: str
        :raises ApiException: Si el token no es válido o está ausente.
        '''
        token = token or getenv('BHEXPRESS_API_TOKEN')
        if not token:
            raise ApiException('Se debe configurar la variable de entorno: BHEXPRESS_API_TOKEN.')
        return str(token).strip()

    def __validate_url(self, url):
        '''
        Valida y retorna la URL base para la API.

        :param str url: URL a validar.
        :return: URL validada.
        :rtype: str
        :raises ApiException: Si la URL no es válida o está ausente.
        '''
        return str(url).strip() if url else getenv('BHEXPRESS_API_URL', self.__DEFAULT_URL).strip()

    def __validate_rut(self):
        '''
        Valida y retorna el RUT del Emisor de BHEs a utilizar.

        :param str rut: RUT a validar.
        :return: RUT validado.
        :rtype: str
        :raises ApiException: Si el RUT no es válido o está ausente.
        '''
        rut = getenv('BHEXPRESS_EMISOR_RUT', '')
        if rut == '':
            raise ApiException('Se debe configurar la variable de entorno: BHEXPRESS_EMISOR_RUT.')
        return str(rut).strip()

    def __generate_headers(self):
        '''
        Genera y retorna las cabeceras por defecto para las solicitudes.

        :return: Cabeceras por defecto.
        :rtype: dict
        '''
        return {
            'User-Agent': 'BHExpress: Cliente de API en Python.',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Token %(token)s' % {'token': self.token},
            'X-Bhexpress-Emisor': self.rut
        }

    def get(self, resource, headers = None):
        '''
        Realiza una solicitud GET a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        '''
        return self.__request('GET', resource, headers = headers)

    def delete(self, resource, headers = None):
        '''
        Realiza una solicitud DELETE a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        '''
        return self.__request('DELETE', resource, headers = headers)

    def post(self, resource, data = None, headers = None):
        '''
        Realiza una solicitud POST a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        '''
        return self.__request('POST', resource, data = data, headers = headers)

    def put(self, resource, data = None, headers = None):
        '''
        Realiza una solicitud PUT a la API.

        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud.
        :param dict headers: Cabeceras adicionales para la solicitud.
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        '''
        return self.__request('PUT', resource, data = data, headers = headers)

    def __request(self, method, resource, data = None, headers = None):
        '''
        Método privado para realizar solicitudes HTTP.

        :param str method: Método HTTP a utilizar.
        :param str resource: Recurso de la API a solicitar.
        :param dict data: Datos a enviar en la solicitud (opcional).
        :param dict headers: Cabeceras adicionales para la solicitud (opcional).
        :return: Respuesta de la solicitud.
        :rtype: requests.Response
        :raises ApiException: Si el método HTTP no es soportado o si hay un error de conexión.
        '''
        api_path = '/api/%(version)s%(resource)s' % {'version': self.version, 'resource': resource}
        full_url = urllib.parse.urljoin(self.url + '/', api_path.lstrip('/'))
        headers = headers or {}
        headers = {**self.headers, **headers}
        if data and not isinstance(data, str):
            data = json.dumps(data)
        try:
            response = requests.request(method, full_url, data = data, headers = headers)
            return self.__check_and_return_response(response)
        except requests.exceptions.ConnectionError as error:
            raise ApiException('Error de conexión: %(error)s' % {'error': error})
        except requests.exceptions.Timeout as error:
            raise ApiException('Error de timeout: %(error)s' % {'error': error})
        except requests.exceptions.RequestException as error:
            raise ApiException('Error en la solicitud: %(error)s' % {'error': error})

    def __check_and_return_response(self, response):
        '''
        Verifica la respuesta de la solicitud HTTP y maneja los errores.

        :param requests.Response response: Objeto de respuesta de requests.
        :return: Respuesta validada.
        :rtype: requests.Response
        :raises ApiException: Si la respuesta contiene un error HTTP.
        '''
        if response.status_code != 200 and self.raise_for_status:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as error:
                try:
                    error = response.json()
                    message = error.get('message', '') or error.get('exception', '') or 'Error desconocido.'
                except json.decoder.JSONDecodeError:
                    message = 'Error al decodificar los datos en JSON: %(response)s' % {'response': response.text}
                raise ApiException('Error HTTP: %(message)s' % {'message': message})
        return response

class ApiException(Exception):
    '''
    Excepción personalizada para errores en el cliente de la API.
    '''

    def __init__(self, message, code = None, params = None):
        '''
        Constructor para la creación de manejo de errores.

        :param str message: Mensaje de error.
        :param int code: Código de error (opcional).
        :param dict params: Parámetros adicionales del error (opcional).
        '''
        self.message = message
        self.code = code
        self.params = params
        super().__init__(message)

    def __str__(self):
        '''
        Devuelve una representación en cadena del error, proporcionando un contexto claro
        del problema ocurrido. Esta representación incluye el prefijo "[BHExpress]",
        seguido del código de error si está presente, y el mensaje de error.

        Si se especifica un código de error, el formato será:
        "[BHExpress] Error {code}: {message}"

        Si no se especifica un código de error, el formato será:
        "[BHExpress] {message}"

        :return: Una cadena que representa el error de una manera clara y concisa.
        '''
        if self.code is not None:
            return '[BHExpress] Error %(code)s: %(message)s' % {'code': self.code, 'message': self.message}
        else:
            return '[BHExpress] %(message)s' % {'message': self.message}

class ApiBase(ABC):
    '''
    Clase base para las clases que consumen la API (wrappers).

    :param str api_token: Token de autenticación para la API.
    :param str api_url: URL base para la API.
    :param str api_version: Versión de la API.
    :param bool api_raise_for_status: Si se debe lanzar una excepción automáticamente para respuestas de error HTTP. Por defecto es True.
    '''

    def __init__(self, api_token = None, api_url = None, api_version = None, api_raise_for_status = True):
        self.client = ApiClient(api_token, api_url, api_version, api_raise_for_status)

