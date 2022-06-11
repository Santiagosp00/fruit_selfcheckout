# Proyecto YOLO para Detección de Frutas para un autocobro

Los baches son un problema muy común en las calles que pueden dañar los vehículos si no se atienden con cuidado. En este proyecto, se buscó customizar un modelo de YOLOv4 para detectar baches en la calle y adicionalmente implementar un sistema que utilice este modelo para detectar y reportar baches encontrados por medio de imágenes.

## Dataset
Para entrenar el modelo de YOLO se utilizó un dataset modificado del que fue creado por Anugrah Akbar que contiene:
* Un total de 1,983 imágenes con distribución 79:21 para train-test
* La parte para train tiene las imágenes aumentadas
* Archivos de anotaciones listos para YOLO darknet

En nuestro caso, hicimos una distribución de 80:15:05 para train-val-test.

Se puede encontrar en esta [liga](https://www.kaggle.com/datasets/anugrahakbar/potholes-detection-for-yolov4).

## Entrenamiento
Para entrenar el modelo se utilizó la librería de [Darknet](https://github.com/AlexeyAB/darknet), donde se ajustaron los siguientes hiperparámetros para personalizar el entrenamiento:
* La única clase a detectar es **Pothole**
* El tamaño de entrada de las imágenes es de **416x416**
* Se usó un batch de **64**

## Para correr el modelo
Dentro de este repositorio se incluyen 3 jupyter notebooks, cada uno con un propósito en el proceso de correr el modelo. Es necesario mencionar que dentro de los notebooks se accesa a Google Drive, por lo que los paths existentes en las distintas celdad deberán de ser editadas al actual al momento de correr, por ello debe de estar corriendo todo en Colab con archivos en la nube de Drive.

### 1. Data_prep
Primeramente se debe correr este archivo, donde su propósito es tomar como entrada el archivo zip con el dataset obtenido de Kaggle. De aquí, este se divide en carpetas para train, test y validation. Además hace la carpeta de data con obj y test necesario para darknet y lo manda a la dirección necesaria para entrenar. 

### 2. Training_notebook
Con el dataset listo, este notebook carga la configuración e inicia el entrenamiento del modelo siguiendo los pasos propuestos por Darknet utilizando un repositorio personal que automatiza el proceso y solo requiere de la edición de un archivo config.

### 3. Inference_test_localizers
Finalmente, aquí se pueden hacer inferencias con el modelo entrenado haciendo una conversión del modelo a Tensorflow usando un repositorio ya hecho que simplifica este paso. Se incluyen algunas funciones auxiliares para dibujar las bounding boxes y labels sobre las imágenes, así como una para generar una matriz de confusión, adaptada para detección de objetos, tras probar el set de test.

En este repositorio se incluyen los archivos en su estado inicial antes de correr, pero cuando se corren se generan nuevas carpetas y archivos de manera automática. En esta [carpeta en Drive](https://drive.google.com/drive/folders/1-XnuVvEzWoMUx0TYYIvuwMWWeIc5B6sN?usp=sharing) se incluye evidencia de cómo es el estado final tras correr todo el proceso de entrenamiento.

## Innovación: Página para reportar baches
Como componente de innovación, se creó una página web que utilice el modelo. Para el frontend se usó [React](https://reactjs.org/) y para el backend se implementó un API usando [Flask](https://flask.palletsprojects.com/en/2.1.x/).

En la página, el usuario puede proporcionar los detalles del bache encontrado, tales como su ubicación, tamaño, entre otras cosas, y subir una imagen. Esta imagen pasa a ser procesada por el modelo de YOLO y con el resultado se genera un reporte, que contiene la imagen creada por el modelo, los detalles que dio el usuario y la fecha.

### Para correr la aplicación
Para correr la aplicación se deben seguir los siguientes pasos:
1. Clonar este repositorio `git clone https://github.com/Gibran98/YOLO-Potholes.git`
2. Entrar a la carpeta de `yolo-flask-deploy`
3. Instalar las dependencias del frontend `npm i` (se necesita tener [Node.js](https://nodejs.org/en/) instalado)
4. Instalar las dependencias del backend `pip install -r requirements.txt` (el archivo se proporciona en este repo)
5. Incluir los folders de `assets` y `variables`, así como el archivo del modelo guardado `saved_model.pb` dentro de la carpeta de `api` (estos 3 se generan al terminar de entrenar el modelo)
6. Correr el servidor de Flask `npm run start-api`
7. Correr la aplicación de React `npm start`

## Dependencias
Se necesitan ciertas dependencias instaladas para correr el modelo y la aplicación web como flask, tensorflow y keras. 

### NOTA: Para el modelo
No se necesita instalar nada siempre y cuando el modelo se esté corriendo en **Google Colab**, pues con las que ahí se proporcionan es suficiente. Implicitamente se instalan las dependencias de los repositorios en la sección de entrenamiento por lo que no se dispone de un archivo txt personal.

### Para la aplicación web
Se incluye el archivo `requirements.txt` con todas las dependencias necesarias para correr el API de Flask. Previamente también se explicó como instalarlas.
