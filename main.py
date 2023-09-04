import flet as ft
from pdf2image import convert_from_path
import os


def main(page: ft.Page):
    page.title = "Convertidor de PDF a Imágenes"

    def on_dialog_result(e: ft.FilePickerResultEvent):
        # print("Selected files:", e.files)
        # print("Selected file or directory:", e.files[0].name)
        b.data = e.files[0].path
        t.value = f"Has seleccionado el archivo:  {e.files[0].name}"
        page.update()

    file_picker = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)

    p = ft.ElevatedButton("Seleccione un archivo...",
                          on_click=lambda _:
                          file_picker.pick_files(
                              allow_multiple=False,
                              allowed_extensions=["pdf"]
                          ),
                          icon="upload_file"
                          )

    t = ft.Text(bgcolor="green", color="white")

    name = ft.TextField(label="Nombre del archivo de salida",
                        hint_text="Nombre del archivo de salida", autofocus=True)
    dd = ft.Dropdown(
        label="Tipo de Imagen",
        hint_text="Selecciona el formato de salida",
        options=[
            ft.dropdown.Option('jpg'),
            ft.dropdown.Option('png'),
            ft.dropdown.Option('png'),
            ft.dropdown.Option('tiff'),
        ],
        # on_change cambiara el valor de t
    )
    containerImages = ft.Row(expand=1, wrap=False, scroll="always")

    download_directory = os.path.expanduser("~/Downloads")

    def button_convert(e):
        pr = ft.ProgressRing(width=16, height=16, stroke_width=2)
        page.add(pr)
        pr.value = 0.5
        if os.path.exists(b.data):
            # Convertir el PDF a imágenes
            images = convert_from_path(b.data)
            # directorio de descargas del usuario
            print(f"{images}")
            # Guardar cada imagen en archivos separados
            for i, imagen in enumerate(images):
                image_path = f"{download_directory}/{name.value}{i}.{dd.value}"
                print(f"{image_path}")
                imagen.save(image_path)

                containerImages.controls.append(
                    ft.Image(
                        src=f"{image_path}",
                        width=300,
                        height=300,
                        fit=ft.ImageFit.CONTAIN,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                    )
                )

                pr.value = 1
                pr.color = "green"

                page.update()
        else:
            print("No se generaron imágenes. Verifica que el PDF tenga contenido.")

    b = ft.ElevatedButton(
        text="Convertir", on_click=button_convert, data="")

    page.add(p, t, name, dd, b, containerImages)


ft.app(target=main)
