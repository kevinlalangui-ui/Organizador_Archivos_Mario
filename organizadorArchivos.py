"""
Autores:
    - Samantha Parra
    - Kevin Lalangui
Descripción: Organizador de archivos
"""

import os
import shutil


def organizadorArchivos():
    ruta = input("Introduce la ruta del archivo a organizar: ")
    ext = input("Introduce la extension del archivo a buscar: (ej: .jpg) ")

    archivos = []
    for f in os.listdir(ruta):
        if f.endswith(ext):
            archivos.append(f)

    if len(archivos) == 0:
        print("No hay archivos encontrados")
        return


    print("Haciendo copia de seguridad")
    shutil.make_archive("respaldo", 'zip', ruta)
    print("Copia de seguridad completada")

    confirmacion = input(f"{len(archivos)} encontrados. ¿Hay una carpeta a la que quieras moverlos?")


    if confirmacion.lower() == "si":
        carpetaDestino = input("Introduce la carpeta de destino: (ej: Imagenes) ")

        destino = os.path.join(ruta, carpetaDestino)
        if not os.path.exists(destino):
            os.makedirs(destino)

        for n in archivos:
            rutaOg= os.path.join(ruta, n)
            rutaNueva = os.path.join(destino, n)
            shutil.move(rutaOg, rutaNueva)

        print("Completado")


organizadorArchivos()
