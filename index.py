import tkinter as tk
from tkinter import Listbox, Button, Entry, messagebox, filedialog
from PIL import Image, ImageTk
from pdf2image import convert_from_path
import os

archivo = ""
# Lista de opciones
opciones_formato = ['jpg', 'jpeg', 'png', 'tiff']
# Función para manejar la selección de la lista


def seleccionar():
    seleccion = lista.curselection()
    if seleccion and len(entry_texto.get()) > 0:
        indice_seleccionado = seleccion[0]
        opcion_seleccionada = opciones_formato[indice_seleccionado]
        label_resultado.config(text="Seleccionaste: " + opcion_seleccionada)

        pdf_path = archivo
        if os.path.exists(pdf_path):
            print(f'Archivo encontrado "{pdf_path}"')
            # Convertir el PDF a imágenes
            images = convert_from_path(pdf_path)
            # directorio de descargas del usuario
            download_directory = os.path.expanduser("~/Downloads")

            # Guardar cada imagen en archivos separados
            for i, image in enumerate(images):
                # Mostrar la miniatura en la etiqueta
                img_miniatura = ImageTk.PhotoImage(image.resize((100, 100)))
                label_miniatura.config(image=img_miniatura)
                label_miniatura.image = img_miniatura
                image.save(
                    f"{download_directory}/{entry_texto.get()}{i}.{opcion_seleccionada}")

            if len(images) > 0:
                print(
                    f"Se convirtieron {len(images)} páginas del PDF a imágenes. \n Se guardaron en {download_directory}")
                messagebox.showinfo(
                    "¡Éxito!", f"Se convirtieron {len(images)} páginas del PDF a imágenes.")
            else:
                print("No se generaron imágenes. Verifica que el PDF tenga contenido.")
        else:
            print(f'La ruta "{pdf_path}" no existe.')
            messagebox.showwarning("Error", "Porfavor seleccione un archivo")
    else:
        messagebox.showwarning(
            "Advertencia", "Porfavor selecciona una extexion o\nun nombre para el archivo de salida")


def ingresar_texto():
    texto_ingresado = entry_texto.get()
    label_resultado_texto.config(text="Texto ingresado: " + texto_ingresado)


def abrir_selector_archivos():
    global archivo
    # que los archivos que se puedan seleccionar sean solo pdf
    archivo = filedialog.askopenfilename(filetypes=(
        ("pdf files", "*.pdf"), ("all files", "*.*")))
    # cambiar el color del boton al seleccionar un archivo y cambiar el texto por la ruta del archivo
    if archivo:
        nombre = archivo.split("/")
        boton_selector.config(bg="#41b883", fg="white", text=nombre[-1])


# Crear una ventana
ventana = tk.Tk()
ventana.title("CONVIERTA SU PDF A IMAGEN")


# Botón para abrir el selector de archivos
boton_selector = tk.Button(
    ventana, text="Seleccionar Archivo", command=abrir_selector_archivos)
boton_selector.pack(pady=10)


# Campo de entrada de texto
label_nombre_archivo = tk.Label(
    ventana, text="Ingrese el nombre para el archivo")
label_nombre_archivo.pack()
entry_texto = Entry(ventana, bg="white", bd=2, relief="solid")
entry_texto.pack(fill="both", expand=True, pady=10, padx=10)

# Crear una lista de opciones
list_label = tk.Label(ventana, text="Seleccione el tipo de formato de salida")
list_label.pack()
lista = Listbox(ventana)
lista.pack(fill="both", expand=True)
lista.anchor()
for opcion in opciones_formato:
    lista.insert(tk.END, opcion)
lista.pack()

# Etiqueta para mostrar la selección
label_resultado = tk.Label(ventana, text="", fg="green")
label_resultado.pack()

# Etiqueta para mostrar la miniatura
label_miniatura = tk.Label(ventana)
label_miniatura.pack()

# Etiqueta para mostrar el texto ingresado
label_resultado_texto = tk.Label(ventana, text="")
label_resultado_texto.pack()

# Crear un botón para confirmar la selección
boton_confirmar = Button(ventana, text="Confirmar", command=seleccionar)
boton_confirmar.pack()


# Configurar el tamaño de la ventana
ventana.update_idletasks()
ventana_width = ventana.winfo_reqwidth()
ventana_height = ventana.winfo_reqheight()
ventana.geometry(f"{ventana_width}x{ventana_height}")

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
