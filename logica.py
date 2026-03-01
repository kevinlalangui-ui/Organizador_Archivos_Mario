import os
import shutil
from tkinter import messagebox
import winshell # NECESARIO PARA LA PAPELERA

# Lee el valor del checkbox.
# True = campos en disabled
# False = campos en normal
def estado_campos(auto_var, entry_extension, entry_destino):
    if auto_var.get():
        entry_extension.config(state="disabled")
        entry_destino.config(state="disabled")
    else:
        entry_extension.config(state="normal")
        entry_destino.config(state="normal")

# En caso de que no existe un zip de respaldo, borra todo el contenido y extrae el zip
def restaurar_respaldo(entry_ruta):
    ruta = entry_ruta.get()

    if not os.path.exists("respaldo.zip"):
        messagebox.showerror("Error", "No existe un respaldo para restaurar")
        return

    try:
        for archivo in os.listdir(ruta):
            rutaArchivo = os.path.join(ruta, archivo)
            if os.path.isfile(rutaArchivo):
                os.remove(rutaArchivo)
            else:
                shutil.rmtree(rutaArchivo)

        shutil.unpack_archive("respaldo.zip", ruta)
        messagebox.showinfo("Restauración", "Archivos restaurados correctamente")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo restaurar: {e}")

# Lee la ruta dle usuario y comprueba que existe.
# Hace una copia de seguridad en un zip.
# Modo Auto On: clasifica todos los archivos en carpetas según su extensión
# Modo Auto Off: mueve los archivos según la extensión que escriba el usuario
def organizar_archivos(auto_var, entry_ruta, entry_extension, entry_destino):
    modoAuto = auto_var.get()
    ruta = entry_ruta.get()
    ext = entry_extension.get()
    carpetaDestino = entry_destino.get()


    if not os.path.exists(ruta):
        messagebox.showerror("Error", "La ruta no existe")
        return

    # modo auto
    if modoAuto:
        try:
            shutil.make_archive("respaldo", 'zip', ruta)
            messagebox.showinfo("Respaldo", "Copia de seguridad completada")
        except:
            messagebox.showerror("Error", "No se pudo crear la copia de seguridad")
            return

        movidos = 0

        for nombre in os.listdir(ruta):
            rutaArchivo = os.path.join(ruta, nombre)

            if os.path.isfile(rutaArchivo):

                # Aquí usamos endswith
                if nombre.endswith(".jpg") or nombre.endswith(".png"):
                    carpeta = "Imagenes"
                elif nombre.endswith(".pdf") or nombre.endswith(".txt"):
                    carpeta = "Documentos"
                else:
                    carpeta = "Otros"

                destino = os.path.join(ruta, carpeta)

                if not os.path.exists(destino):
                    os.makedirs(destino)

                shutil.move(rutaArchivo, os.path.join(destino, nombre))
                movidos += 1

        messagebox.showinfo("Completado", f"{movidos} archivos organizados automáticamente")
        return


    archivos = []
    for f in os.listdir(ruta):
        if f.endswith(ext):
            archivos.append(f)

    if len(archivos) == 0:
        messagebox.showinfo("Información", "No hay archivos encontrados")
        return

    try:
        shutil.make_archive("respaldo", 'zip', ruta)
        messagebox.showinfo("Respaldo", "Copia de seguridad completada")
    except:
        messagebox.showerror("Error", "No se pudo crear la copia de seguridad")
        return

    if carpetaDestino != "":
        destino = os.path.join(ruta, carpetaDestino)

        if not os.path.exists(destino):
            os.makedirs(destino)

        for n in archivos:
            rutaOg = os.path.join(ruta, n)
            rutaNueva = os.path.join(destino, n)
            shutil.move(rutaOg, rutaNueva)

        messagebox.showinfo("Completado", f"{len(archivos)} archivos movidos correctamente")
    else:
        messagebox.showinfo("Aviso", "No se indicó carpeta destino :(")


def recuperar_de_papelera(entry_archivo_papelera):
    nombre_archivo = entry_archivo_papelera.get()

    if not nombre_archivo:
        messagebox.showwarning("Aviso", "Ingresa el nombre del archivo a buscar en la papelera.")
        return

    try:
        papelera = list(winshell.recycle_bin())
        encontrado = False

        for item in papelera:
            if os.path.basename(item.original_filename()) == nombre_archivo:
                winshell.undelete(item.original_filename())
                encontrado = True
                messagebox.showinfo("Éxito", f"'{nombre_archivo}' fue restaurado por Windows a su carpeta original.")
                break

        if not encontrado:
            messagebox.showinfo("Aviso", f"No se encontró '{nombre_archivo}' en la Papelera de Windows.")

    except Exception as e:
        messagebox.showerror("Error", f"Error al acceder a la papelera: {e}")
