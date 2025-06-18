import csv
import json
import random
import re
import sys

import pandas as pd

from colorama import Fore, Style
from inputimeout import inputimeout, TimeoutOccurred

# TODO Test
# TODO Refactorizar

def main():
    """
    Esta función ejecuta en bucle el programa hasta que el usuario decide salir.
    """
    esta_funcionando = True

    while esta_funcionando:
        try:
            mostrar_menu()
            if 0 < elegir_accion() < 4: # Si introduce un número fuera de los proporcionados no entra en seguir() y vuelve al menu.
                esta_funcionando = seguir()
        except ValueError:
            print("Debe ingresar un Numero dentro del rango de opciones mostradas. Volviendo al menu.")
        except IndexError:
            print("No puedes introducir campos vacíos o fuera de rango. Volviendo al menu.")
        except KeyError:
            print("Materia elegida no valida. Volviendo al menu.")

def mostrar_menu():
    """
    Esta función muestra el menu de opciones habilitadas.
    """
    print("""
    ====== Menu ======
        1.Empezar
        2.Ranking
        3.Salir
    ==================
    """)

def elegir_accion():
    """
    Esta función determina la tarea elegida por el usuario.

    Returns:
        int: opción elegida por el usuario
    """
    opc = int(input("Elija una Opción: "))
    match opc:
        case 1: hacer_examen(elegir_materia())
        case 2: ver_clasificacion()
        case 3:
                print("Saliendo...")
                sys.exit()
        case _: print("Debe ingresar un Numero dentro del rango de opciones mostradas.")
    return opc

def seguir():
    """
    Esta función solicita al usuario si desea seguir en el programa o salir.

    Returns:
        boolean: True si quiere seguir. False si desea salir.
    """
    respuesta = input("¿Quiere volver al menu? (S/N)").upper().strip()
    if respuesta == "S":
        return True
    print("\nSaliendo! Hasta otra!")
    return False

def cargar_preguntas():
    """
    Esta función accede al fichero que contiene las preguntas.

    Returns:
        json: Archivo con todas las preguntas.
    """
    with open("../data/preguntas.json", "r", encoding="utf-8") as file:
        return json.load(file)

def elegir_materia():
    """
    Esta función permite elegir de qué materia quiere hacer el usuario el examen.

    Returns:
        str: Devuelve la materia seleccionada
    """
    print("""
    ===== Materias =====
        1. Matemáticas
        2. Historia
        3. Ciencias
        4. Lengua
        5. Geografía
    ====================
    """)

    opc = int(input("Elige una materia: "))
    materias = list(cargar_preguntas().keys())
    return materias[opc - 1] if opc > 0 else None

def hacer_examen(opc):
    """
    Esta función ejecuta el examen. Muestra las preguntas, las opciones y si es correcta la respuesta dada por el usuario.

    Args:
        opc (str): Materia seleccionada.
    """
    preguntas = cargar_preguntas()[opc]
    total_preguntas = 10
    indice_lista_preguntas = random.sample(range(0, len(preguntas)), total_preguntas)
    numero_aciertos = 0
    TIEMPO = 10

    for i in indice_lista_preguntas:
        pregunta = preguntas[i]
        print(pregunta["pregunta"] + "\n")

        for n in range(len(pregunta["opciones"])):
            print(pregunta["opciones"][n])

        try:
            respuesta = inputimeout(prompt="\n" + "Introduce tu respuesta: ", timeout=TIEMPO).upper().strip()
            numero_aciertos += comprobar_respuesta(respuesta, pregunta["respuesta_correcta"])
        except TimeoutOccurred:
            print("Se te acabo el tiempo!\n")


    resultado_final(total_preguntas, numero_aciertos)
    guardar_puntuacion(numero_aciertos)

def comprobar_respuesta(resp, correcta):
    """
    Esta función comprueba si la respuesta dada por el usuario es igual que la contenida.

    Args:
        resp (str): Respuesta introducida por el usuario.
        correcta (str): Respuesta correcta.

    Returns:
        int: 1 si son iguales 0 si no.
    """
    if resp == correcta:
        print(Fore.GREEN + "Correcto" + Style.RESET_ALL + "\n")
        return 1
    print(Fore.RED + "Has fallado" + Style.RESET_ALL + "\n")
    return 0

def resultado_final(total_preguntas, aciertos):
    """
    Esta función muestra por pantalla un mensaje de como le fue el examen al usuario.

    Args:
        total_preguntas (int): Número total de preguntas del examen.
        aciertos (int): Aciertos totales del usuario.

    Returns:
        tipo: Descripción de lo que retorna la función.
    """
    valoracion = "Lo has hecho genial !!" if aciertos >= 7 else ("Bien!" if aciertos >= 5 else "Necesitas practicar más. Tu puedes !!")

    print(f"""
    ===== Resultado Final Test =====
    
        Total de Preguntas = {total_preguntas}
        Numero de Aciertos = {aciertos}
        Porcentaje de Aciertos = {(aciertos / total_preguntas) * 100}%
        Valoración final = {valoracion}
        
    =================================
    """)

def guardar_puntuacion(aciertos):
    """
    Esta función pregunta al usuario si quiere registrar su marca dentro del historial.

    Args:
        aciertos (int): Aciertos totales del usuario.
    """
    resp = input("¿Quieres guardar tu puntuación?: (S/N)").upper().strip()

    match resp:
        case "S": almacenar_datos_partida(aciertos)
        case _: print("\nLa proxima vez será!!\n")

def almacenar_datos_partida(aciertos):
    """
    Esta función almacena el nombre y la puntuación del usuario en el historial.

    Args:
        aciertos (int): Aciertos totales del usuario.

    Returns:
        _: Nada, es solo para que termine la ejecución de la función.
    """

    while True:
        nombre_usuario = input("Introduce tu nombre para el ranking: ").title().strip()

        if not re.fullmatch(r"[A-Za-z ]+", nombre_usuario):
            print("El nombre solo puede contener letras.\n")
        else:
            if not comprobar_existencia(nombre_usuario):
                with open("../data/ranking.csv", "a") as file:
                    file.write(f"\n{nombre_usuario},{aciertos}")
                    print("Marca recogida.\n")
                    return
            else:
                print("Ya existe el nombre.")

        probar = input("¿Quieres probar de nuevo?: (S/N)").strip().upper()
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
            print(f"\t{i}.{nombre} -> {calificacion}")
        print()

if __name__ == "__main__":
    main()