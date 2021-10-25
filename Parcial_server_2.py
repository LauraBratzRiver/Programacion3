from urllib import parse
from http.server import HTTPServer, BaseHTTPRequestHandler

#importando las librerias
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import tensorflow_datasets as tfds
import math
import numpy as np
import matplotlib as plt


temperaturas = pd.read_csv("datos.csv" , sep=",")
print(temperaturas)

fahrenheit = temperaturas["fahrenheit"]
celsius = temperaturas["celsius"]

modelo = tf.keras.Sequential()
modelo.add(tf.keras.layers.Dense(units=1, input_shape=[1]))

#compilar el modelo
modelo.compile(optimizer=tf.keras.optimizers.Adam(1), loss='mean_squared_error')

#puerto 3007

#entrenamiento de nuestro modelo de Aprendizaje
historial = modelo.fit(fahrenheit, celsius, epochs=200, verbose=0)


#hacer predicciones
k = modelo.predict([35])
print(k)
#Carga de datos de mnist (set de entrenamiento y de pruebas)
dataset, metadata = tfds.load('mnist', as_supervised=True, with_info=True)
train_dataset, test_dataset = dataset['train'], dataset['test']



num_train_examples = metadata.splits['train'].num_examples
num_test_examples = metadata.splits['test'].num_examples

#Normalizar: Numeros de 0 a 255, que sean de 0 a 1
def normalize(images, labels):
    images = tf.cast(images, tf.float32)
    images /= 255
    return images, labels

train_dataset = train_dataset.map(normalize)
test_dataset = test_dataset.map(normalize)

#Estructura de la red
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28,28,1)),
    tf.keras.layers.Dense(64, activation=tf.nn.relu),
    tf.keras.layers.Dense(64, activation=tf.nn.relu),
    tf.keras.layers.Dense(10, activation=tf.nn.softmax) #para clasificacion
])

#Indicar las funciones a utilizar
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

#Aprendizaje por lotes de 32 cada lote
BATCHSIZE = 32
train_dataset = train_dataset.repeat().shuffle(num_train_examples).batch(BATCHSIZE)
test_dataset = test_dataset.batch(BATCHSIZE)

#Realizar el entrenamiento
model.fit(
    train_dataset, epochs=5,
    steps_per_epoch=math.ceil(num_train_examples/BATCHSIZE) #No sera necesario pronto
)



#Clase para definir el servidor http. Solo recibe solicitudes POST.
class servidorBasico(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Peticion GET recibida")
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        #Enviar respuesta
        self.wfile.write("Programacion III, PARCIAL II".encode())

    def do_POST(self):
        print("Peticion recibida")

        #Obtener datos de la peticion y limpiar los datos
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode().replace('pixeles=', '')
        data = parse.unquote(data)

        #Realizar transformacion para dejar igual que los ejemplos que usa MNIST
        arr = np.fromstring(data, np.float32, sep=",")
        arr = arr.reshape(28,28)
        arr = np.array(arr)
        arr = arr.reshape(1,28,28,1)

        #Realizar y obtener la prediccion
        prediction_values = modelo.predict(arr, batch_size=1)
        prediction = str(np.argmax(prediction_values))
        print("Prediccion final: " + prediction)

        #Regresar respuesta a la peticion HTTP
        self.send_response(200)
        #Evitar problemas con CORS
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(prediction.encode())

#Iniciar el servidor en el puerto 8000 y escuchar por siempre
#Si se queda colgado, en el admon de tareas buscar la tarea de python y finalizar tarea
print("Iniciando el servidor... en el puerto 3007")
server = HTTPServer(('localhost', 3007 ), servidorBasico)
server.serve_forever()
