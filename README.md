# Chatbot-uami

Chatbot creado para servicios escolares utilizando RASA y TF-IDF

## Arquitectura

![image](https://github.com/ivanhue/chatbot-uami/assets/47096604/d00e6ae5-4ca1-4169-80b9-d38f91e077ca)


## Deployment

### Instalación

Descargar código:

![image-1](https://github.com/ivanhue/chatbot-uami/assets/47096604/f355f328-9f74-4f8f-8826-075fecf3c310)


Descargar [docker](https://www.docker.com/).

Una vez descargados ambos y docker corriendo de fondo se debe ejecutar el siguiente comando para habilitar la [api](https://rasa.com/docs/rasa/http-api/) del chatbot.

```bash
docker-compose up
```

Si se desea cerrar y eliminar la api, se debe forzar el cierre con `ctrl+C` en la terminal donde se habilitó y ejecutar el siguiente comando:

```bash
docker-compose down
```

### Uso básico.

Para mandar un mensaje se debe enviar un mensaje de este estilo con un método POST:

```json
{
  "sender": "test_user",
  "message": "Hi there!",
}
```

Y se recibirá una respuesta similar a esta:

```json
[
    {
        "recipient_id": "test_user",
        "text": "Hey! How are you?"
    }
]
```

## Guia de desarrollo.

### Instalación.

Una vez descargado el código se recomienda utilizar [conda](https://www.anaconda.com/), recordando habilitar la configuración de las **variables de entorno** para su uso en la linea de comandos del sistema operativo.

![image-2](https://github.com/ivanhue/chatbot-uami/assets/47096604/353fd582-311e-41fe-a35a-12e55633a9ff)

Una vez instalando conda se debe comprobar su correcto funcionamiento en la linea de comandos.

```bash
conda --version
```

Mostrará la version de conda instalado

![image-3](https://github.com/ivanhue/chatbot-uami/assets/47096604/28bd9772-1636-42c6-a456-e2e4081a8697)

A continuación se debe crear un [entorno](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment) nuevo para configurar todos los requisitos, donde `chatbot-name` que se va usar para activar cada vez que se quiera utilizar el chatbot. La versión de python debe ser alguna de las que [soporta RASA](https://rasa.com/docs/rasa/installation/environment-set-up/#:~:text=Python%20Environment%20Setup&text=Currently%2C%20rasa%20supports%20the%20following,is%20not%20functional%20in%203.4.)

```bash
conda create -n chatbot-name python=3.9
conda activate chatbot-name
```

Una vez activado el entorno se deberán instalar las dependencias con el siguiente comando

```bash
pip install rasa scikit-learn nlkt pandas
```

### Detección de inteciones
Para mejorar la detección y clasificación de intenciones se debe de modificar los archivos dentro de la carpeta `data`. Se recomienda revisar la [documentación](https://rasa.com/docs/rasa/training-data-format) para mayor claridad y los [tutoriales](https://www.youtube.com/watch?v=Ap62n_YAVZ8&list=PL75e0qA87dlEjGAc9j9v3a5h1mxI2Z9fi) oficiales.

### Recuperador
En caso de que la recuperación de urls sea incorrecta o se desee mejorar se recomienda consultar el [repositorio](https://github.com/ivanhue/analisis-tfidf) donde se analiza el modelo y revisar la documentación de [TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html), así como revisar [articulos](https://medium.com/@cmukesh8688/tf-idf-vectorizer-scikit-learn-dbc0244a911a) al respecto

### Conjunto de datos
Para actualizar o crear conjunto de datos se recomienda revisar el [repositorio](https://github.com/ivanhue/scraping_urls) que contiene el algoritmo para recolección y filtrado de páginas web.

### Posibles errores.

#### Instalando dependencias.
Es posible que surjan errores con la instalacion de dependencias, para verificar si el problema es instalar RASA se puede ejecutar el siguiente comando que arrojará un error.

```bash
pip install rasa
```

El error más común es asociado a no tener el entorno de desarrollo configurado adecuadamente, para checar si esta configurado adecuadamente, se debe checar las siguientes configuraciones.

1. Conda este activado y funcionando en entorno seleccionado. Se mostrará con un asterisco el entorno activo.
```bash
conda info --envs
```
2. Checando la version de python. Debe ser alguna que [soporte RASA](https://rasa.com/docs/rasa/installation/environment-set-up/#:~:text=Python%20Environment%20Setup&text=Currently%2C%20rasa%20supports%20the%20following,is%20not%20functional%20in%203.4.)
```bash
python --version
```
o
```bash
python3 --version
```
Si alguna otra dependencia muestra problemas se podrá probar instalando una version distinta de la misma o verificando si se requiere alguna otra dependencia más para su instalación.

