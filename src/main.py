import json
import sys

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

    print(cargar_preguntas())

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
        case 1: print("1")
        case 2: print("2")
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

if __name__ == "__main__":
    main()