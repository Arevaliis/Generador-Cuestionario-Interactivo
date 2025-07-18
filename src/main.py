import sys

from colorama import Fore, Style

from examen import hacer_examen
from ranking import ver_clasificacion
from utils import limpiar_consola

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