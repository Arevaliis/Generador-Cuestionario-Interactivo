import csv
import json
import os
import platform
import random
import re
import sys
import time

import pandas as pd

from colorama import Fore, Style
from inputimeout import inputimeout, TimeoutOccurred

# ╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                         ESTE PROGRAMA DEBE EJECUTARSE DESDE LA TERMINAL (CMD O BASH)                         ║
# ║                   NO LO EJECUTES DESDE LA TERMINAL INTEGRADA DEL IDE (NI PYCHARM, NI VS CODE)                ║
# ║                      PROVOCARIA QUE EL MODULO OS E INPUTUMEOUT NO FUNCIONARAN CORRECTAMENTE                  ║
# ║                                                                                                              ║
# ║                              ⇒ UBÍCATE EN: Generador-Cuestionarios-Interactivo\src                           ║
# ║                                         ⇒ EJECUTA: python main.py                                            ║
# ╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

def main():
    """
    Esta función ejecuta en bucle el programa hasta que el usuario decide salir.
    """
    limpiar_consola()
    esta_funcionando = True

    while esta_funcionando:
        mostrar_menu_principal()
        try:
            opc = elegir_accion()

            if opc != -1:
                esta_funcionando = ejecutar_accion(opc)

        except KeyboardInterrupt:
            limpiar_consola()
            print(Fore.RED + "El programa ha sido interrumpido de forma manual" + Style.RESET_ALL)
            sys.exit()

def mostrar_menu_principal():
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
    try:
        return int(input("Elija una Opción: "))
    except ValueError:
        limpiar_consola()
        print(Fore.RED + "Error -> Solo se puede ingresar valores numéricos." + Style.RESET_ALL)
        return -1

def ejecutar_accion(opc):
    """
    Esta función ejecuta la tarea elegida por el usuario.

    Args:
        opc (int): Opción elegida por el usuario (1, 2 o 3).
    """

    limpiar_consola()

    match opc:
        case 1: hacer_examen()
        case 2: ver_clasificacion()
        case 3:
                print(Fore.GREEN + "\nSaliendo! Hasta otra!" + Style.RESET_ALL)
                sys.exit() # Permite finalizar programa sin que vuelva nuevamente al menu principal
        case _:
                print(Fore.RED + "Error -> Debe ingresar un valor numérico válido (1-2-3)." + Style.RESET_ALL )
                return True
    return seguir()

def cargar_preguntas():
    """
    Esta función accede al fichero que contiene las preguntas.

    Returns:
        dict: Archivo.json con todas las preguntas.
    """
    with open("../data/preguntas.json", "r", encoding="utf-8") as file:
        return json.load(file)

def mostrar_opciones_materias():
    print("""
        ===== Materias =====
            1. Matemáticas
            2. Historia
            3. Ciencias
            4. Lengua
            5. Geografía
            6. Salir
        ====================
        """)

def elegir_materia():
    """
    Esta función permite elegir de qué materia quiere hacer el usuario el examen.

    Returns:
        str: Devuelve la materia seleccionada
    """
    mostrar_opciones_materias()
    volver_a_preguntar = True

    while volver_a_preguntar:
        try:
            opc = int(input("Elija una materia: "))

            if opc in range(1,7):
                return opc

            limpiar_consola()
            print(Fore.RED + "Error -> Debe ingresar un valor numérico válido (1-2-3-4-5)." + Style.RESET_ALL)
            mostrar_opciones_materias()

        except ValueError:
            limpiar_consola()
            print(Fore.RED + "Error -> Ha ingresado un valor no numérico. Debe ingresar un valor numérico" + Style.RESET_ALL)
            mostrar_opciones_materias()

def hacer_examen():
    """
    Esta función ejecuta el examen. Muestra las preguntas, las opciones y si es correcta la respuesta dada por el usuario.
    """
    indice_materia = elegir_materia()

    if indice_materia == 6:
        limpiar_consola()
        return

    materia = list(cargar_preguntas().keys())[indice_materia]
    preguntas = cargar_preguntas()[materia]
    total_preguntas = 10
    indice_lista_preguntas = random.sample(range(0, len(preguntas)), total_preguntas)
    numero_aciertos = 0
    tiempo = 10

    for i in indice_lista_preguntas:
        limpiar_consola()
        print(f"\nTienes {tiempo} segundos por pregunta para responder.\n")
        pregunta = preguntas[i]
        print(pregunta["pregunta"] + "\n")

        for n in range(len(pregunta["opciones"])):
            print(pregunta["opciones"][n])

        try:
            respuesta = inputimeout(prompt="\n" + "Introduce tu respuesta: ", timeout=tiempo).upper().strip()
            numero_aciertos += comprobar_respuesta(respuesta, pregunta["respuesta_correcta"])
            time.sleep(0.5)
        except TimeoutOccurred:
            print(Fore.RED + "Se te acabo el tiempo!\n" + Style.RESET_ALL)
            time.sleep(0.7)

    resultado_final(total_preguntas, numero_aciertos)
    guardar_puntuacion(numero_aciertos)


def comprobar_respuesta(resp, correcta):
    """
    Esta función comprueba si la respuesta dada por el usuario es igual que la contenida en las soluciones.

    Args:
        resp (str): Respuesta introducida por el usuario.
        correcta (str): Respuesta correcta.

    Returns:
        int: 1 si son iguales si no devolverá 0.
    """
    if resp == correcta:
        print(Fore.GREEN + "Correcto\n" + Style.RESET_ALL)
        return 1
    print(Fore.RED + "Has fallado\n" + Style.RESET_ALL)
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
    limpiar_consola()
    porcentaje = (aciertos / total_preguntas) * 100
    valoracion = "Lo has hecho genial !!" if porcentaje >= 80 else ("Bien!" if porcentaje >= 50 else "Necesitas practicar más. Tu puedes !!")

    print(f"""
    ===== Resultado Final Test =====
    
        Total de Preguntas = {total_preguntas}
        Numero de Aciertos = {aciertos}
        Porcentaje de Aciertos = {porcentaje}%
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

def limpiar_consola():
    """
    Esta función ejecuta un comando para limpiar la consolo en función del sistema operativo usado
    """
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def seguir():
    """
    Esta función solicita al usuario si desea seguir en el programa o salir.

    Returns:
        boolean: True si quiere seguir. False si desea salir.
    """
    respuesta = input("¿Quiere volver al menu? (S/N)").upper().strip()
    if respuesta == "S":
        limpiar_consola()
        return True
    limpiar_consola()
    print(Fore.GREEN + "\nSaliendo! Hasta otra!" + Style.RESET_ALL)
    return False

if __name__ == "__main__":
    main()