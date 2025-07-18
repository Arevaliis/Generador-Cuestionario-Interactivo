import json
import random
import time

from inputimeout import inputimeout, TimeoutOccurred
from colorama import Fore, Style

from utils import limpiar_consola
from ranking import guardar_puntuacion

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

            if opc in range(1, 7):
                return opc

            limpiar_consola()
            print(Fore.RED + "Error -> Debe ingresar un valor numérico válido (1-2-3-4-5-6)." + Style.RESET_ALL)
            mostrar_opciones_materias()

        except ValueError:
            limpiar_consola()
            print(
                Fore.RED + "Error -> Ha ingresado un valor no numérico. Debe ingresar un valor numérico" + Style.RESET_ALL)
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
    valoracion = "Lo has hecho genial !!" if porcentaje >= 80 else (
        "Bien!" if porcentaje >= 50 else "Necesitas practicar más. Tu puedes !!")

    print(f"""
    ===== Resultado Final Test =====

        Total de Preguntas = {total_preguntas}
        Numero de Aciertos = {aciertos}
        Porcentaje de Aciertos = {porcentaje}%
        Valoración final = {valoracion}

    =================================
    """)