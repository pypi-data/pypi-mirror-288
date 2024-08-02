BHExpress: Cliente de API en Python
=====================================

.. image:: https://badge.fury.io/py/bhexpress.svg
    :target: https://pypi.org/project/bhexpress
.. image:: https://img.shields.io/pypi/status/bhexpress.svg
    :target: https://pypi.org/project/bhexpress
.. image:: https://img.shields.io/pypi/pyversions/bhexpress.svg
    :target: https://pypi.org/project/bhexpress
.. image:: https://img.shields.io/pypi/l/bhexpress.svg
    :target: https://raw.githubusercontent.com/bhexpress/bhexpress-api-client-python/master/COPYING

Cliente para realizar la integración con los servicios web de `BHExpress <https://www.bhexpress.cl>`_ desde Python.

Instalación y actualización
---------------------------

Instalar usando un entorno virtual y PIP con:

.. code:: shell

    python3 -m venv venv
    source venv/bin/activate
    pip install bhexpress

Actualizar usando PIP con:

.. code:: shell

    pip install bhexpress --upgrade

Modo de uso
-----------

Se recomienda ver los ejemplos para más detalles. Lo que se muestra aquí es sólo
una idea, y muy resumida:

Lo más simple, y recomendado, es usar una variable de entorno con el
`token del usuario <https://bhexpress.cl/usuarios/perfil#token>`_,
el cual será reconocida automáticamente por el cliente:

.. code:: python

    from bhexpress.api_client.bhe.boletas import Boleta

    client = Boleta()

    boletas = client.listar()
    print(boletas)

Lo que hizo el ejemplo anterior es listar boletas emitidas en un resultado e imprimir dicho resultado en consola.

Variables de entorno
--------------------

La aplicación y las pruebas hacen uso de variables de entornos. Si quieres usar
estos, debes tenerlas creadas. En Windows 10 se hace con:

.. code:: shell

    set BHEXPRESS_API_URL="https://bhexpress.cl"
    set BHEXPRESS_API_TOKEN="" # aquí el token obtenido en https://bhexpress.cl/usuarios/perfil#token
    set BHEXPRESS_EMISOR_RUT="" # aquí el RUT del emisor de las BHE

Ejemplo de definición de variables de entorno en la consola de Linux:

.. code:: shell

    export BHEXPRESS_API_URL="https://bhexpress.cl"
    export BHEXPRESS_API_TOKEN="" # aquí el token obtenido en https://bhexpress.cl/usuarios/perfil#token
    export BHEXPRESS_EMISOR_RUT="" # aquí el RUT del emisor de las BHE

Pruebas
-------

Las pruebas utilizan un archivo llamado `test.env`, que sirve para definir todas las variables de entorno
necesarias para ejecutar estas pruebas. Las pruebas se crearon para probar los ejemplos vistos previamente
en el capítulo `Ejemplos`.

Estas pruebas utilizan `unittest`, se ejecutan con el archivo `run.py`, y dependiendo de cómo se configure
`test.env`, se pueden omitir ciertas pruebas. Asegúrate de definir `BHEXPRESS_API_URL`, `BHEXPRESS_API_TOKEN`
y `BHEXPRESS_EMISOR_RUT` en `test.env`, o no podrás efectuar las pruebas.

Para ejecutar las pruebas unitarias, debes ejecutar el siguiente código en consola desde la raíz del proyecto:

.. code:: shell

    python tests/run.py

Si quieres ejecutar una prueba específica, deberás especificar el nombre y ruta:

.. code:: shell

    python tests/run.py boletas.test_boletas.TestBheBoletas.test1_listar

Para ejecutar otros ejemplos, debes reemplazar `test1_listar` por el nombre de alguna de las otras pruebas descritas posteriormente.

A continuación se pondrán instrucciones de cómo probar el cliente de API de Python:

* `test1_listar()`:
    - Prueba que permite obtener un listado de todas las boletas emitidas a través de BHExpress usando algunos filtros.
    - Variables necesarias: `TEST_LISTAR_PERIODO`, `TEST_LISTAR_CODIGORECEPTOR`
    - Variable de ejecución: `Ninguna`
* `test2_emitir()`:
    - Prueba que permite emitir una BHE a un receptor.
    - Variables necesarias: `TEST_EMITIR_FECHA_EMIS`, `TEST_EMITIR_EMISOR`, `TEST_EMITIR_RECEPTOR`, `TEST_EMITIR_RZNSOC_REC`, `TEST_EMITIR_DIR_REC`, `TEST_EMITIR_COM_REC`
    - Variable de ejecución: `TEST_EMITIR_EMISOR`
* `test3_pdf()`:
    - Prueba que permite obtener una BHE y convertirla a un PDF.
    - Variables necesarias: `Ninguna`
    - Variable de ejecución: `TEST_PDF_PROBAR`
* `test4_email()`:
    - Prueba que permite enviar un email a un destinatario con una BHE específica.
    - Variables necesarias: `TEST_EMAIL_NUMEROBHE`, `TEST_EMAIL_CORREO`
    - Variable de ejecución: `TEST_EMAIL_NUMEROBHE` y `TEST_EMAIL_CORREO`
* `test5_anular()`:
    - Prueba que permite anular una BHE existente.
    - Variables necesarias: `Ninguna`
    - Variables de ejecución: `TEST_ANULAR_PROBAR`

Las `variables necesarias` son aquellas variables que se necesitan para ejecutar las pruebas.
Las `variables de ejecución` son aquellas variables que permitirán ejecutar u omitir las pruebas a las que pertenecen.
Si las variables de ejecución tienen un valor específico o son texto en blanco, entonces la prueba será omitida, pero no fallida.

Licencia
--------

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la GNU Lesser General Public License (LGPL) publicada
por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
o (a su elección) cualquier versión posterior de la misma.

Este programa se distribuye con la esperanza de que sea útil, pero SIN
GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
Public License (LGPL) para obtener una información más detallada.

Debería haber recibido una copia de la GNU Lesser General Public License
(LGPL) junto a este programa. En caso contrario, consulte
`GNU Lesser General Public License <http://www.gnu.org/licenses/lgpl.html>`_.

Enlaces
-------

- `Sitio web BHExpress <https://www.bhexpress.cl>`_.
- `Código fuente en GitHub <https://github.com/bhexpress/bhexpress-api-client-python>`_.
- `Paquete en PyPI <https://pypi.org/project/bhexpress>`_.
- `Documentación en Read the Docs <https://bhexpress.readthedocs.io/es/latest>`_.
