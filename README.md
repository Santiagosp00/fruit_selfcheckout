# Proyecto YOLO para Detección de Frutas para un autocobro

En la actualidad es más notorio el acceso a zonas de autocobro en los supermercados donde la facilidad de pasar tus productos es mucho más rápido que las filas en el método convencional. Sin embargo, un punto potencial que no se ha cubrido en la automatización de la sección de frutas y verduras, donde estas aún se necesitan pesar y seleccionar de manera manual. Con este proyecto pretendemos diseñar un modelo de detección de frutas para simular un ambiente de autocobro con la finalidad de que el consumidor solo deba dejar la fruta y verdura un tiempo determinado y se hará el autocobro. 

## Dataset
Para entrenar el modelo de YOLO se utilizó un dataset personal que involucra 5 productos, jitomate, naranja, toronja, plátano y manzana. De este dataset se tiene que hay:
* Un total de 877 imágenes con distribución de 80:15:05 para los diferentes sets de imágenes
* La parte para train tiene las imágenes aumentadas
* Archivos de anotaciones listos para YOLO darknet

En nuestro caso, hicimos una distribución de 80:15:05 para train-val-test. Este se encuentra en un archivo zip dentro del repositorio. Las etiquetas y la aumentación de datos se realizó con el software Roboflow. 

## Entrenamiento
Para entrenar el modelo se utilizó la librería de [Darknet](https://github.com/AlexeyAB/darknet), donde se ajustaron los siguientes hiperparámetros para personalizar el entrenamiento:
* Las clases a detectar son **apple**,**banana**,**grapefruit**,**orange**,**tomato**
* El tamaño de entrada de las imágenes es de **416x416**
* Se usó un batch de **64**

## Para correr el modelo
Dentro de este repositorio se incluyen 3 jupyter notebooks, cada uno con un propósito en el proceso de correr el modelo. Es necesario mencionar que dentro de los notebooks se accesa a Google Drive, por lo que los paths existentes en las distintas celdas deberán de ser editadas al actual al momento de correr, por ello debe de estar corriendo todo en Colab con archivos en la nube de Drive.

### 1. Data_prep
Primeramente se debe correr este archivo, donde su propósito es tomar como entrada el archivo zip con el dataset preparado de Roboflow. De aquí, este ya está dividido en las carpetas necesarias. Lo principal es la creacción de la carpeta de data con obj y test necesario para darknet y lo manda a la dirección necesaria para entrenar. 

### 2. Training_notebook
Con el dataset listo, este notebook carga la configuración e inicia el entrenamiento del modelo siguiendo los pasos propuestos por Darknet utilizando un repositorio personal que automatiza el proceso y solo requiere de la edición de un archivo config.

### 3. Inference_test_localizers
Finalmente, aquí se pueden hacer inferencias con el modelo entrenado haciendo una conversión del modelo a Tensorflow usando un repositorio ya hecho que simplifica este paso. Se incluyen algunas funciones auxiliares para dibujar las bounding boxes y labels sobre las imágenes, así como una para generar una matriz de confusión, adaptada para detección de objetos, tras probar el set de test.

En este repositorio se incluyen los archivos en su estado inicial antes de correr, pero cuando se corren se generan nuevas carpetas y archivos de manera automática.

## Aplicación: Página para simular el autocobro
Como aplicación de los resultados de nuestro modelo, se creó una página web que utilice el mismo. Para la creación de este, se utilizó como base el repositorio de Github [yolov5-flask](https://github.com/robmarkcole/yolov5-flask), donde se hicieron modificaciones en el framework (Pytorch a Tensroflow), el acceso a los archivos y la visualización de las páginas html. 

En la página, el usuario proporciona una imagen de frutas y al cargarla el modelo infiere los productos que hay e imprime los resultados como lo son el tipo de fruta o verdura, la cantidad detectada y el precio unitario del mismo. Este último es una estimación dado que en la actualidad los precios son pero peso en lugar de cantidad. Por último genera el total de compra de la fruta detectada.

### Para correr la aplicación
Para correr la aplicación se deben seguir los siguientes pasos:
1. Clonar este repositorio `git clone https://github.com/Santiagosp00/fruit_selfcheckout.git`
2. Entrar a la carpeta de `yolov4-flask`
3. Crear un ambiente virtual e instalar las dependencias de la aplicación
  - python3 -m venv flask_env
  - source flask_env/bin/activate
  - (venv) $ pip install -r requirements.txt
6. Incluir los folders de `assets` y `variables`, así como el archivo del modelo guardado `saved_model.pb` dentro de la carpeta de `model` (estos 3 se generan al terminar de entrenar el modelo). **Nota: Para simplificación del repositorio, estos ya están incluidos**
7. Correr la aplicación con el comando `python3 webapp.py --port 5000`

## Dependencias
Se necesitan ciertas dependencias instaladas para correr el modelo y la aplicación web como flask, tensorflow y keras. 

### NOTA: Para el modelo
No se necesita instalar nada siempre y cuando el modelo se esté corriendo en **Google Colab**, pues con las que ahí se proporcionan es suficiente. Implicitamente se instalan las dependencias de los repositorios en la sección de entrenamiento por lo que no se dispone de un archivo txt personal.

### Para la aplicación web
Se incluye el archivo `requirements.txt` con todas las dependencias necesarias para correr el API de Flask. Previamente también se explicó como instalarlas.
