import tkinter as tk
from tkinter import Listbox, Button, Entry , messagebox, filedialog
from pdf2image import convert_from_path
import os

archivo = ""
# Lista de opciones
opciones_formato = ['jpg', 'jpeg', 'png', 'tiff']
# Función para manejar la selección de la lista
def seleccionar():
    seleccion = lista.curselection()
    if seleccion and len(entry_texto.get())>0:
        indice_seleccionado = seleccion[0]
        opcion_seleccionada = opciones_formato[indice_seleccionado]
        label_resultado.config(text="Seleccionaste: " + opcion_seleccionada)

        pdf_path = archivo
        if os.path.exists(pdf_path):
            print(f'Archivo encontrado "{pdf_path}"')
            # Convertir el PDF a imágenes
            images = convert_from_path(pdf_path)

            # Guardar cada imagen en archivos separados
            for i, image in enumerate(images):
                image.save(f'{entry_texto.get()}{i + 1}.jpg', 'JPEG')
            
            if len(images) > 0:
                print(f"Se convirtieron {len(images)} páginas del PDF a imágenes.")
                messagebox.showinfo("¡Éxito!", f"Se convirtieron {len(images)} páginas del PDF a imágenes.")
            else :
                print("No se generaron imágenes. Verifica que el PDF tenga contenido.") 
        else:
            print(f'La ruta "{pdf_path}" no existe.')
    else :
        messagebox.showwarning("Advertencia", "Porfavor selecciona una extexion o\nun nombre para el archivo de salida")
        

def ingresar_texto():
    texto_ingresado = entry_texto.get()
    label_resultado_texto.config(text="Texto ingresado: " + texto_ingresado)

def abrir_selector_archivos():
    global archivo 
    archivo = filedialog.askopenfilename()

# Crear una ventana
ventana = tk.Tk()
ventana.title("CONVIERTA SU PDF A IMAGEN")
ventana.geometry("400x350")

# Botón para abrir el selector de archivos
boton_selector = tk.Button(ventana, text="Seleccionar Archivo", command=abrir_selector_archivos)
boton_selector.pack(pady=10)


# Campo de entrada de texto
label_nombre_archivo = tk.Label(ventana, text="Ingrese el nombre para el archivo")
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

# Etiqueta para mostrar el texto ingresado
label_resultado_texto = tk.Label(ventana, text="")
label_resultado_texto.pack()

# Crear un botón para confirmar la selección
boton_confirmar = Button(ventana, text="Confirmar", command=seleccionar)
boton_confirmar.pack()

# Etiqueta para mostrar la selección
label_resultado = tk.Label(ventana, text="")
label_resultado.pack()

# Iniciar el bucle principal de la aplicación
ventana.mainloop()