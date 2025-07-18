import csv
import re
import time

import pandas as pd
from colorama import Fore, Style

from utils import limpiar_consola

def guardar_puntuacion(aciertos):
    """
    Esta función pregunta al usuario si quiere registrar su marca dentro del historial.

    Args:
        aciertos (int): Aciertos totales del usuario.
    """
    resp = input("¿Quieres guardar tu puntuación?: (S/N)").upper().strip()

    match resp:
        case "S": almacenar_datos_partida(aciertos)
        case _:
                limpiar_consola()
                print("\nLa proxima vez será!!\n")

def almacenar_datos_partida(aciertos):
    """
    Esta función almacena el nombre y la puntuación del usuario en el historial.

    Args:
        aciertos (int): Aciertos totales del usuario.

    Returns:
        _: Nada, es solo para que termine la ejecución de la función.
    """
    limpiar_consola()

    while True:
        nombre_usuario = input("Introduce tu nombre para el ranking, " + Fore.RED + "solo se aceptan letras en el nombre: " + Style.RESET_ALL).title().strip()

        if not re.fullmatch(r"[A-Za-z ]+", nombre_usuario):
            print(Fore.RED + "El nombre solo puede contener letras.\n" + Style.RESET_ALL)
            time.sleep(1.5)
            limpiar_consola()

        else:
            if not comprobar_existencia(nombre_usuario):
                with open("../data/ranking.csv", "a") as file:
                    file.write(f"\n{nombre_usuario},{aciertos}")
                    print(Fore.GREEN + "Marca recogida.\n" + Style.RESET_ALL)
                    return

            print(Fore.RED + "Ya existe el nombre." + Style.RESET_ALL)
            time.sleep(1.5)
            limpiar_consola()

        probar = input("¿Quieres probar de nuevo?: (S/N)").strip().upper()
        limpiar_consola()
        if not probar == "S":
            print("No se ha registrado la puntuación.\n")
            return

def comprobar_existencia(nombre):
    """
        Esta función comprueba si ya existe el nombre dentro del ranking.

        Args:
            nombre (str): Nombre con el que quiere registrarse el usuario en el ranking.

        Returns:
            boolean: Nada, es solo para que termine la ejecución de la función.
        """
    df_ranking = pd.read_csv("../data/ranking.csv")
    return df_ranking.nombre.isin([nombre]).any()

def ordenar_ranking():
    """
    Esta función hace uso de la libreria pandas para facilitar la tarea de ordenar la clasificación.
    """
    df_ranking = pd.read_csv("../data/ranking.csv")
    df_ordenado = df_ranking.sort_values(by=df_ranking.columns[1], ascending=False)
    df_ordenado.to_csv("../data/ranking.csv", index=False)

def ver_clasificacion():
    """
    Esta función nos muestra la clasificación.
    """
    ordenar_ranking()
    with open("../data/ranking.csv", "r") as file:
        ranking = csv.reader(file, delimiter=",")

        print("\nNombre -- Calificación")
        for i, row in enumerate(ranking, 0):
            if i == 0:
                continue
            nombre, calificacion = row
            print(f"   {i}.{nombre} -> {calificacion}")
        print()