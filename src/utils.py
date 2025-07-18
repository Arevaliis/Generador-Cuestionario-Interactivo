import os
import platform

def limpiar_consola():
    """
    Esta función ejecuta un comando para limpiar la consolo en función del sistema operativo usado
    """
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")