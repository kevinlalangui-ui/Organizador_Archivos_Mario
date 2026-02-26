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



def organizar_archivos():
    ruta = entry_ruta.get()
    ext = entry_extension.get()

    if not os.path.exists(ruta):
        messagebox.showerror("Error", "La ruta no existe")
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


ventana = tk.Tk()
ventana.title("Organizador de Archivos")
ventana.geometry("400x250")

tk.Label(ventana, text="Ruta de la carpeta:").pack()
entry_ruta = tk.Entry(ventana, width=50)
entry_ruta.pack()

tk.Label(ventana, text="Extensión (ej: .jpg):").pack()
entry_extension = tk.Entry(ventana, width=20)
entry_extension.pack()




ventana.mainloop()