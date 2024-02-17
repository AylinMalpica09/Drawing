import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Variables globales para la gestión de eventos del ratón
dibujar_lineas = False
dibujar_linea_recta = False
dibujar_circulo = False
dibujar_cuadrado = False
x_inicio, y_inicio = None, None
img = 255 * np.ones((512, 512, 3), dtype=np.uint8)  # Crear una imagen en blanco usando OpenCV
dibujos = []  # Lista para guardar los dibujos creados
polilinea_actual =[]

def activar_dibujar_lineas():
    global dibujar_lineas, dibujar_circulo, dibujar_cuadrado, dibujar_linea_recta
    dibujar_lineas = True
    dibujar_circulo = False
    dibujar_cuadrado = False
    dibujar_linea_recta = False

def activar_dibujar_linea_recta():
    global dibujar_lineas, dibujar_circulo, dibujar_cuadrado, dibujar_linea_recta
    dibujar_linea_recta = True
    dibujar_lineas = False
    dibujar_circulo = False
    dibujar_cuadrado = False

def activar_dibujar_circulo():
    global dibujar_lineas, dibujar_circulo, dibujar_cuadrado, dibujar_linea_recta
    dibujar_circulo = True
    dibujar_lineas = False
    dibujar_cuadrado = False
    dibujar_linea_recta = False

def activar_dibujar_cuadrado():
    global dibujar_lineas, dibujar_circulo, dibujar_cuadrado, dibujar_linea_recta
    dibujar_cuadrado = True
    dibujar_lineas = False
    dibujar_circulo = False
    dibujar_linea_recta = False

def dibujar(evento):
    global x_inicio, y_inicio, dibujar_circulo, dibujar_lineas, dibujar_cuadrado, dibujar_linea_recta, img, dibujos, radio
    img_temp = img.copy()  # Copiar la imagen original
    dibujar_figuras(img_temp)  # Dibujar todas las figuras guardadas en la lista
    if dibujar_circulo:
        if x_inicio is not None and y_inicio is not None:
            radio = int(((evento.x - x_inicio) ** 2 + (evento.y - y_inicio) ** 2) ** 0.5)
            cv2.circle(img_temp, (x_inicio, y_inicio), radio, (0, 0, 0), 2)
    elif dibujar_lineas:
        if x_inicio is not None and y_inicio is not None:
            if polilinea_actual:
                cv2.polylines(img_temp, [np.array(polilinea_actual, np.int32)], False, (0, 0, 0), 2)
            polilinea_actual.append((evento.x, evento.y))  # Agregar el punto al final de la polilínea actual
    elif dibujar_cuadrado:
        if x_inicio is not None and y_inicio is not None:
            cv2.rectangle(img_temp, (x_inicio, y_inicio), (evento.x, evento.y), (0, 0, 0), 2)
    elif dibujar_linea_recta:
        if x_inicio is not None and y_inicio is not None:
            cv2.line(img_temp, (x_inicio, y_inicio), (evento.x, evento.y), (0, 0, 0), 2)
    if polilinea_actual:
        for i in polilinea_actual:
            cv2.polylines(img_temp, [np.array(polilinea_actual, np.int32)], False, (0, 0, 0), 2)
            
    mostrar_img(img_temp)

def dibujar_figuras(img_temp):
    for dibujo in dibujos:
        if dibujo[0] == 'linea':
            cv2.line(img_temp, dibujo[1], dibujo[2], (0, 0, 0), 2)
        elif dibujo[0] == 'circulo':
            #print(polilinea_actual)
            cv2.circle(img_temp, dibujo[1], dibujo[2], (0, 0, 0), 2)
        elif dibujo[0] == 'cuadrado':
            cv2.rectangle(img_temp, dibujo[1], dibujo[2], (0, 0, 0), 2)

def mostrar_img(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(image=img_pil)
    panel.img_tk = img_tk
    panel.config(image=img_tk)

def limpiar_img():
    global img, dibujos
    img = 255 * np.ones((512, 512, 3), dtype=np.uint8)
    dibujos = []  # Limpiar la lista de dibujos
    mostrar_img(img)

def establecer_inicio(evento):
    global x_inicio, y_inicio
    x_inicio, y_inicio = evento.x, evento.y

def establecer_fin(evento):
    global x_inicio, y_inicio, dibujos
    if dibujar_lineas or dibujar_circulo or dibujar_cuadrado or dibujar_linea_recta:
        if x_inicio is not None and y_inicio is not None:
            if dibujo_actual()=="circulo":
                dibujos.append((dibujo_actual(), (x_inicio, y_inicio), radio))
            else:
                dibujos.append((dibujo_actual(), (x_inicio, y_inicio), (evento.x, evento.y)))
            x_inicio, y_inicio = None, None
            

def dibujo_actual():
    if dibujar_lineas:
        return 'lineas'
    elif dibujar_circulo:
        return 'circulo'
    elif dibujar_cuadrado:
        return 'cuadrado'
    elif dibujar_linea_recta:
        return 'linea'

# Crear una ventana de Tkinter
root = tk.Tk()
root.title("Dibujar Figuras")

# Crear un panel para mostrar la imagen
panel = tk.Label(root)
panel.pack(padx=10, pady=10)

# Mostrar la imagen inicial
mostrar_img(img)

# Crear botones para seleccionar la opción de dibujo
boton_linea = tk.Button(root, text="Mano alzada", command=activar_dibujar_lineas)
boton_linea.pack(side=tk.LEFT, padx=5)

boton_linea = tk.Button(root, text="Dibujar Línea", command=activar_dibujar_linea_recta)
boton_linea.pack(side=tk.LEFT, padx=5)

boton_circulo = tk.Button(root, text="Dibujar Círculo", command=activar_dibujar_circulo)
boton_circulo.pack(side=tk.LEFT, padx=5)

boton_cuadrado = tk.Button(root, text="Dibujar Cuadrado", command=activar_dibujar_cuadrado)
boton_cuadrado.pack(side=tk.LEFT, padx=5)

boton_limpiar = tk.Button(root, text="Limpiar", command=limpiar_img)
boton_limpiar.pack(side=tk.LEFT, padx=5)

# Asignar eventos de clic del ratón a la imagen para establecer el inicio y el fin del dibujo
panel.bind("<Button-1>", establecer_inicio)
panel.bind("<ButtonRelease-1>", establecer_fin)

# Asignar evento de movimiento del ratón a la imagen para dibujar figuras
panel.bind("<B1-Motion>", dibujar)

# Ejecutar el bucle principal de Tkinter
root.mainloop()