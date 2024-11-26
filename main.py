import ttkbootstrap as ttk
from ttkbootstrap.constants import * 
from tkinter import filedialog, messagebox
from PIL import Image, ImageEnhance, ImageOps
import random

def convertir_a_pixelart(imagen, tamano_pixel=None):
    """Convierte una imagen a estilo pixel art."""
    if tamano_pixel:
        tamano_pixel = int(tamano_pixel)
        imagen = imagen.resize((tamano_pixel, tamano_pixel), Image.NEAREST)
        imagen = imagen.resize(
            (imagen.width * tamano_pixel, imagen.height * tamano_pixel), Image.NEAREST
        )
    return imagen

def generar_variacion(imagen):
    """Genera una variación de la imagen pixelada."""
    # Opciones de variación: brillo, contraste, rotación, espejo
    variacion = imagen.copy()
    
    if random.choice([True, False]):  # Cambiar brillo
        enhancer = ImageEnhance.Brightness(variacion)
        variacion = enhancer.enhance(random.uniform(0.8, 1.2))
    
    if random.choice([True, False]):  # Cambiar contraste
        enhancer = ImageEnhance.Contrast(variacion)
        variacion = enhancer.enhance(random.uniform(0.8, 1.2))
    
    if random.choice([True, False]):  # Rotación aleatoria
        variacion = variacion.rotate(random.choice([0, 90, 180, 270]))
    
    if random.choice([True, False]):  # Voltear horizontalmente
        variacion = ImageOps.mirror(variacion)
    
    return variacion

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=(("Imágenes", "*.png *.jpg *.jpeg *.gif"), ("Todos los archivos", "*.*"))
    )
    if archivo:
        entrada_var.set(archivo)

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta de destino")
    if carpeta:
        salida_var.set(carpeta)

def procesar_imagen():
    archivo = entrada_var.get()
    carpeta = salida_var.get()
    tamano_pixel = tamano_var.get()
    num_variaciones = int(variaciones_var.get() or 0)

    if not archivo or not carpeta:
        messagebox.showerror("Error", "Debe seleccionar un archivo y una carpeta.")
        return

    try:
        # Abrir la imagen
        imagen = Image.open(archivo)
        # Convertir a pixel art con tamaño especificado
        pixelart = convertir_a_pixelart(imagen, tamano_pixel if tamano_pixel else None)
        # Guardar la imagen principal
        nombre_base = archivo.split('/')[-1]
        nombre_salida = f"{carpeta}/pixelart_{nombre_base}"
        pixelart.save(nombre_salida)
        
        # Generar variaciones
        for i in range(1, num_variaciones + 1):
            variacion = generar_variacion(pixelart)
            nombre_variacion = f"{carpeta}/pixelart_variacion_{i}_{nombre_base}"
            variacion.save(nombre_variacion)

        messagebox.showinfo(
            "Éxito",
            f"Imagen convertida y guardada con {num_variaciones} variación(es).\nCarpeta: {carpeta}"
        )
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo procesar la imagen.\n{e}")

# Interfaz gráfica con ttkbootstrap
root = ttk.Window(themename="solar")  # Cambiá "solar" por otros temas como "darkly", "flatly", etc.
root.title("Conversor a PixelArt")
root.geometry("400x580")
root.iconbitmap("pixel.ico")

# Variables de entrada/salida
entrada_var = ttk.StringVar()
salida_var = ttk.StringVar()
tamano_var = ttk.StringVar()  # Tamaño de píxeles
variaciones_var = ttk.StringVar()  # Número de variaciones

# Widgets
ttk.Label(root, text="Seleccionar imagen:", font=("Helvetica", 12)).pack(pady=10)
ttk.Entry(root, textvariable=entrada_var, width=40).pack(pady=5)
ttk.Button(root, text="Buscar", command=seleccionar_archivo, bootstyle=PRIMARY).pack()

ttk.Label(root, text="Seleccionar carpeta de destino:", font=("Helvetica", 12)).pack(pady=10)
ttk.Entry(root, textvariable=salida_var, width=40).pack(pady=5)
ttk.Button(root, text="Buscar", command=seleccionar_carpeta, bootstyle=PRIMARY).pack()

ttk.Label(root, text="Tamaño de píxeles (opcional):", font=("Helvetica", 12)).pack(pady=10)
ttk.Entry(root, textvariable=tamano_var, width=20).pack(pady=5)
ttk.Label(root, text="(Si no se especifica, usará el tamaño original)", font=("Helvetica", 10)).pack()

ttk.Label(root, text="Número de variaciones (opcional):", font=("Helvetica", 12)).pack(pady=10)
ttk.Entry(root, textvariable=variaciones_var, width=20).pack(pady=5)
ttk.Label(root, text="(Dejar vacío para no generar variaciones)", font=("Helvetica", 10)).pack()

ttk.Button(root, text="Convertir a PixelArt", command=procesar_imagen, bootstyle=SUCCESS).pack(pady=20)

root.mainloop()
