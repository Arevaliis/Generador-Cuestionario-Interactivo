import csv
import json
import random
import sys

import pandas as pd
from colorama import Fore, Style

# TODO Usar Excepciones
# TODO Guardar puntacion
# TODO Sistema Ranking
# TODO Tiempo limite preguntas
# TODO Test
# TODO Documentación
# TODO Archivo Requirement.txt
# TODO READme.md
# TODO Archivos .gitignore?

def main():
    esta_funcionando = True

    while esta_funcionando:
        try:
            mostrar_menu()
            elegir_accion()
            esta_funcionando = seguir()
        except ValueError:
            print("Debe ingresar un Numero del 1-3")
        except IndexError:
            print("Error. No puedes introducir campos vacíos. Volviendo al menu.")

def mostrar_menu():
    print("""
    ====== Menu ======
        1.Empezar
        2.Ranking
        3.Salir
    ==================
    """)

def elegir_accion():
    opc = int(input("Elija una Opción: "))
    match opc:
        case 1: hacer_examen(elegir_materia())
        case 2: ver_clasficacion()
        case 3:
                print("Saliendo...")
                sys.exit()
        case _: print("Debe ingresar un Numero del 1-3")

def seguir():
    respuesta = input("¿Quiere volver al menu? (S/N)").upper()
    return respuesta.startswith("S")

def cargar_preguntas():
    with open("../data/preguntas.json", "r", encoding="utf-8") as file:
        return json.load(file)

def elegir_materia():
    print("""
    ===== Materias =====
        1. Matemáticas
        2. Historia
        3. Ciencias
        4. Lengua
        5. Geografía
    ====================
    """)
    opc = int(input(("Elije una materia: ")))
    materias = list(cargar_preguntas().keys())
    return materias[opc - 1]

def hacer_examen(opc):
    preguntas = cargar_preguntas()[opc]
    TOTAL_PREGUNTAS = 10
    lista_preguntas = random.sample(range(0, len(preguntas)), TOTAL_PREGUNTAS)
    numero_aciertos = 0

    for i in lista_preguntas:
        pregunta = preguntas[i]
        print(pregunta["pregunta"] + "\n")

        for n in range(len(pregunta["opciones"])):
            print(pregunta["opciones"][n])

        respuesta = input("\n" + "Introduce tu respuesta: ").upper().strip()
        numero_aciertos += comprobar_respuesta(respuesta, pregunta["respuesta_correcta"] )

    resultado_final(TOTAL_PREGUNTAS, numero_aciertos)
    guardar_puntuacion(numero_aciertos)

def comprobar_respuesta(resp, correcta):
    if resp == correcta:
        print(Fore.GREEN + "Correcto" + Style.RESET_ALL + "\n")
        return 1
    else:
        print(Fore.RED + "Has fallado" + Style.RESET_ALL + "\n")
        return 0

def resultado_final(total_preguntas, aciertos):
    valoracion = "Lo has hecho genial !!" if aciertos >= 7 else ("Bien!" if aciertos >= 5 else "Necesitas practicas mas. Tu puedes !!")

    print(f"""
    ===== Resultado Final Test =====
    
        Total de Preguntas = {total_preguntas}
        Numero de Aciertos = {aciertos}
        Porcentaje de Aciertos = {(aciertos / total_preguntas) * 100}%
        Valoracion final = {valoracion}
        
    =================================
    """)

def guardar_puntuacion(aciertos):
    resp = input("¿Quieres guardar tu puntuacion?: (S/N)").upper().strip()

    match resp:
        case "S": almacenar_datos_partida(aciertos)
        case "_": print("De acuerdo")

def almacenar_datos_partida(aciertos):
    nombre_usuario = input("Introduce tu nombre para el ranking: ").capitalize()

    with open("../data/ranking.csv", "a") as file:
        return file.write(f"{nombre_usuario} , {aciertos}")

def ordenar_ranking():
    df_ranking = pd.read_csv("../data/ranking.csv")
    df_ordenado = df_ranking.sort_values(by=df_ranking.columns[1], ascending=False)
    df_ordenado.to_csv("../data/ranking.csv", index=False)

def ver_clasficacion():
    ordenar_ranking()
    with open("../data/ranking.csv", "r") as file:
        ranking = csv.reader(file, delimiter=",")

        print("Nombre -- Calificación")
        for i, row in enumerate(ranking, 0):
            if i == 0:
                continue
            nombre, calificacion = row
            print(f"\t{i}.{nombre.title()} -> {calificacion}")

if __name__ == "__main__":
    main()
