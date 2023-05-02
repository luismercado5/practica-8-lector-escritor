# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 20:46:25 2023

@author: luis mercado
"""

import threading
import random
import time
import tkinter as tk

root = tk.Tk()
root.title("Simulador de lectura/escritura")
# Variables compartidas
data = 0  # número consecutivo que va aumentando cada vez que se escribe
writing = False  # indica si un escritor está escribiendo

# Función para el hilo del escritor
def writer_thread():
    global data, writing
    while True:
        # Espera aleatoria antes de escribir
        time.sleep(random.choice([0.5, 1, 2]))
        # Adquiere el bloqueo de escritura
        while writing:
            time.sleep(0.5)
        writing = True
        # Escribe en el archivo y actualiza el número consecutivo
        with open('archivo.txt', 'a') as f:
            f.write(str(data) + '\n')
            data += 1
        # Libera el bloqueo de escritura
        writing = False
        print("esta escribiendo")

# Función para el hilo del lector
def reader_thread():
    while True:
        # Espera aleatoria antes de leer
        time.sleep(random.choice([1, 1.5, 2]))
        # Adquiere el bloqueo de lectura
        with open('archivo.txt', 'r') as f:
            while writing:
                time.sleep(0.5)
            # Lee el contenido del archivo y lo imprime
            print("esta leyendo")
            print(f.read())

label = tk.Label(root, text="Lectura: Detenida | Escritura: Detenida")
label.pack()

def start_writing():
    global writing_thread
    writing_thread = threading.Thread(target=writer_thread)
    writing_thread.start()
    label.config(text="Lectura: Detenida | Escritura: En curso")

def stop_writing():
    global writing_thread
    writing_thread.stop()
    label.config(text="Lectura: Detenida | Escritura: Detenida")

def start_reading():
    global reading_thread
    reading_thread = threading.Thread(target=reader_thread)
    reading_thread.start()
    label.config(text="Lectura: En curso | Escritura: Detenida")

def stop_reading():
    global reading_thread
    reading_thread.stop()
    label.config(text="Lectura: Detenida | Escritura: Detenida")

btn_start_writing = tk.Button(root, text="Iniciar escritura", command=start_writing)
btn_stop_writing = tk.Button(root, text="Detener escritura", command=stop_writing)
btn_start_reading = tk.Button(root, text="Iniciar lectura", command=start_reading)
btn_stop_reading = tk.Button(root, text="Detener lectura", command=stop_reading)

btn_start_writing.pack()
btn_stop_writing.pack()
btn_start_reading.pack()
btn_stop_reading.pack()


# Crea los hilos para los escritores y lectores
writers = [threading.Thread(target=writer_thread) for i in range(2)]
readers = [threading.Thread(target=reader_thread) for i in range(2)]

# Inicia los hilos
for t in writers + readers:
    t.start()

# Espera a que todos los hilos terminen
for t in writers + readers:
    t.join()
