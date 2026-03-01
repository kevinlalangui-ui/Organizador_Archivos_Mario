import tkinter as tk
from logica import estado_campos, organizar_archivos, restaurar_respaldo,recuperar_de_papelera


def iniciar_interfaz():
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
    checkbox_auto = tk.Checkbutton(ventana, text="Auto", variable=auto,
                                   command=lambda: estado_campos(auto, entry_extension, entry_destino))
    checkbox_auto.pack(pady=5)

    tk.Label(ventana, text="Carpeta destino (opcional):").pack()
    entry_destino = tk.Entry(ventana, width=30)
    entry_destino.pack()

    tk.Button(ventana, text="Organizar",
              command=lambda: organizar_archivos(auto, entry_ruta, entry_extension, entry_destino)).pack(pady=15)

    tk.Button(ventana, text="Restaurar respaldo",
              command=lambda: restaurar_respaldo(entry_ruta)).pack()

#papelera
    tk.Label(ventana, text="Archivo a recuperar de la papelera:").pack(pady=(10, 0))
    entry_archivo_papelera = tk.Entry(ventana, width=30)
    entry_archivo_papelera.pack()

    tk.Button(ventana, text="Recuperar de Papelera",
              command=lambda: recuperar_de_papelera(entry_archivo_papelera)).pack(pady=5)

    estado_campos(auto, entry_extension, entry_destino)
    ventana.mainloop()