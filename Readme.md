### Descripción del Proyecto

Este proyecto es una API para gestionar registros de llamadas utilizando un archivo CSV como fuente de datos. La API está construida con FastAPI y utiliza pandas para la manipulación de datos.

### Comentarios de Desarrollador
1. La decision de resolver el ejercicio en forma de API ya que considero que es la practica mas cercana al dia a dia en un contexto laboral
2. Para el caso de las llamadas a amigos, decidi mostrar el costo en todas las llamadas y manejar las llamadas gratuitas como un _**descuento**_, para eso agregue al contrato de respuesta dos nuevos key `gross_total`, que representa el valor SIN descuento y `friends_discount` que representa en negativo el valor descontado en las primeras 10 llamadas gratuitas a amigos. La razon de esta decision es porque considero que de esta manera es mucho más escalable a futuro (otros descuentos) y además aporta claridad a los clientes sobre sus consumos.
3. Para el ejercicio contemplé dos posibles casos de error que devuelven un 404:
   - El usuario consultado no existe en el servicio remoto de consulta de usuarios
   - El usuario existe, pero no tiene llamadas realizadas en el periodo dado, en este caso se devuelve un 404 para mantener consistencia con la definición de la API y además hace mas facil la depuración de posibles errores.
4. El archivo CSV fue usado como una fuente de datos en lugar de ser enviado por medio de parametros en el request, si puede ser especificado su path a traves del archivo .env. De igual manera se desarrolló un mecanismo el cual permitiría cambiar la fuente de datos facilmente sin afectar la logica de negocio.

### Definiciones
#### Usuario: Es el usuario de la línea telefónica, consta de un nombre, una dirección, un
número de teléfono y una lista de amigos (lista de números de teléfonos)

#### Nros de teléfono: Formato +549XXXXXXXXXX, los primeros 2 dígitos luego del +
representan el país: en este caso +54 es Argentina

Hay un servicio disponible para consultar usuarios en
https://fn-interview-api.azurewebsites.net/users/:phoneNumber

#### Llamadas:
Están representadas por:
- Orígen: Número de teléfono de quien llama
- Destino: Número al cual se llamó
- Fecha: En que se realizó la llamada, formato AAAA-MM-DD HH:MM:SS -

#### Duración: 
Cuánto tiempo duró esa llamada, expresada en segundos
Pueden ser de 3 tipos: Nacionales, Internacionales y Amigos

#### Tarifas:
- Nacionales ($2.5 por llamada)
- Internacionales ($0.75 x segundo)
- Amigos (Gratis hasta 10 llamadas)
### Dependencias

- **Python**: Lenguaje de programación utilizado.
- **FastAPI**: Framework para construir APIs web rápidas y eficientes.
- **pandas**: Biblioteca para la manipulación y análisis de datos.
- **uvicorn**: Servidor ASGI para ejecutar la aplicación FastAPI.

### Instalación de Dependencias

Para instalar las dependencias, ejecuta el siguiente comando:

```bash
pip install -r requirements.txt
```

### Configuración del Entorno

Las configuracion se puede personalizar en el archivo .env o .env.test segun corresponda

### Ejecutar la Aplicación

Para ejecutar la aplicación localmente, utiliza el siguiente comando:

```bash
uvicorn main:app --reload
```

### Ejecutar Pruebas

Para ejecutar las pruebas, utiliza el siguiente comando:

```bash
pytest
```

### Levantar la Aplicación con Docker Compose

Asegúrate de tener Docker y Docker Compose instalados. 
Para levantar la aplicación con Docker Compose, ejecuta los siguientes comandos:

```bash
$ docker-compose build
$ docker-compose up
```

Esto levantará la aplicación en el puerto 8000.


### Ejecución 
Una vez levantado en docker puede acceder a un `swagger` directamente desde [127.0.0.1:8000/docs]().

O si lo prefiere puede enviar request directamente al servicio desde **CURL**, **POSTMAN** o alguna herramienta similar 

### Ejemplos de Request y Response

#### Request

```json
{
    "method": "POST",
    "url": "/get-invoice/",
    "body": {
        "phone_number": "+5411111111111",
        "date_from": "2025-01-01",
        "date_to": "2025-02-01"
    }
}
```

#### Ejemplo de Response Exitoso

```json
{
    "status_code": 200,
    "body": {
        "calls": [{
            "amount": 346.5,
            "duration": 462,
            "phone_number": "+191167980952",
            "timestamp": "2025-01-01T04:02:45Z"
        }],
        "friends_discount": -346.5,
        "gross_total": 346.5,
        "total": 0.0,
        "total_friends_seconds": 462.0,
        "total_international_seconds": 462.0,
        "total_national_seconds": 0.0,
        "user": {
            "address": "7431 Berge Coves",
            "name": "Deshawn Goodwin",
            "phone_number": "+5411111111111"
        }
    }
}
```

#### Ejemplo de Response de Error - Usuario No Encontrado

```json
{
    "status_code": 404,
    "body": {
        "detail": "User not found"
    }
}
```

#### Ejemplo de Response de Error - No Hay Llamadas en el Rango

```json
{
    "status_code": 404,
    "body": {
        "detail": "No calls found for the given phone number"
    }
}
```



### Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

- `src/`: Contiene el código fuente de la aplicación.
  - `main.py`: Archivo principal que define la aplicación FastAPI y los endpoints.
  - `Config/`: Contiene configuraciones y dependencias. permite por ejemplo determinar cual implementacion CallRegistryBaseConnector se va a utilizar,
              lo que permitiria cambiar entre distintas conexiones a base de datos o conectore a otros servicios sin afectar la logica de negocio
  - `Connectors`: Contiene los diferentes conectores a las fuente de datos (BD, Api externa, CSV)
    - `CallsRegistryBaseConnector/`: Clase Abstracta que define los metodos de consulta y la cual es referenciada desde los servicios que la refieran
    - `CallsRegistryCSVConnector/`: Implementacion de CallsRegistryBaseConnector para permitir consultar los datos desde un archivo CSV especificado en .env
  - `Dto/`: Contiene los modelos de datos utilizados en la API.
  - `Services/`: Contiene la lógica de negocio y servicios de la aplicación.
    - `CallProcessor/`: Contiene la implementación del patrón de diseño Strategy para el procesamiento de llamadas.
      - `CallProcessorStrategy`: Define una interfaz común para todas las estrategias de procesamiento de llamadas.
                                  Contiene métodos abstractos calculate y is_applicable que deben ser implementados por las estrategias concretas.
      - `NationalCallProcessorStrategy/`,
      - `InternationalCallProcessorStrategy/`,
      - `FriendsCallProcessorStrategy/`:implementan la interfaz CallProcessorStrategy.
                                        Cada clase concreta proporciona su propia implementación de los métodos calculate y is_applicable.
      - `CallProcessorContext/`: Mantiene una referencia a una lista de objetos CallProcessorStrategy.
                                  Permite agregar estrategias, establecer información del usuario y procesar llamadas utilizando las estrategias agregadas.
                                  Proporciona un método get_results para obtener los resultados acumulados de todas las estrategias
- `Tests/`: Contiene los archivos de prueba para la aplicación.
- `requirements.txt`: Lista de dependencias del proyecto.
- `Readme.md`: Documentación del proyecto.

### Flujo del Proyecto

1. El cliente realiza una solicitud POST al endpoint `/get-invoice/` 
2. FastAPI recibe la solicitud y la pasa al servicio `PhoneInvoiceService` a través de la dependencia `get_service`.
3. `PhoneInvoiceService` procesa la solicitud, consulta los datos necesarios y calcula la factura del teléfono.
4. La respuesta se devuelve al cliente con los detalles de la factura.

