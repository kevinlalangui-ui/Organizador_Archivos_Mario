"""
Autores:
    - Samantha Parra
    - Kevin Lalangui
Descripción: Organizador de archivos con interfaz gráfica
"""

import os
import shutil
import tkinter as tk
from tkinter import messagebox


# Lee el valor del checkbox.
# True = campos en disabled
# False = campos en normal
def estado_campos():
    if auto.get():
        entry_extension.config(state="disabled")
        entry_destino.config(state="disabled")
    else:
        entry_extension.config(state="normal")
        entry_destino.config(state="normal")

# En caso de que no existe un zip de respaldo, borra todo el contenido y extrae el zip
def restaurar_respaldo():
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
def organizar_archivos():
    modoAuto = auto.get()
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

# VENTANA, CAMPOS, BOTONES
ventana = tk.Tk()
ventana.title("Organizador de Archivos")
ventana.geometry("400x250")
auto = tk.BooleanVar(value=False)

tk.Label(ventana, text="Ruta de la carpeta:").pack()
entry_ruta = tk.Entry(ventana, width=50)
entry_ruta.pack()

tk.Label(ventana, text="Extensión (ej: .jpg):").pack()
entry_extension = tk.Entry(ventana, width=20)
entry_extension.pack()

# su checkbox de auto
checkbox_auto = tk.Checkbutton(ventana, text="Auto", variable=auto, command=estado_campos)
checkbox_auto.pack(pady=5)

tk.Label(ventana, text="Carpeta destino (opcional):").pack()
entry_destino = tk.Entry(ventana, width=30)
entry_destino.pack()

tk.Button(ventana, text="Organizar", command=organizar_archivos).pack(pady=15)
tk.Button(ventana, text="Restaurar respaldo", command=restaurar_respaldo).pack()



estado_campos()
ventana.mainloop()
# mainloop mantiene la ventana abierta