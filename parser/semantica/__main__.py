"""Verificador semantico: python -m parser.semantica programa.qc.

Retorna 0 si el programa es correcto y 1 si hay errores lexicos,
sintacticos o semanticos.
"""

import argparse
import sys
from pathlib import Path

from parser.analizador import Analizador
from parser.asa_impresion import imprimir_preorden
from parser.integracion import explorar_para_parser
from parser.semantica.analisis import verificar_semantica
from parser.semantica.errores_semanticos import reportar
from parser.semantica.impresion_tabla import imprimir_cambio_parcial
from parser.semantica.tabla_simbolos import TablaSimbolos


def analizar_fuente(fuente, ruta, mostrar_tabla=False):
    entrada = explorar_para_parser(fuente)
    if not entrada.apta:
        for error in entrada.errores_lexicos:
            print(f"{ruta}: {error}", file=sys.stderr)
        return None
    resultado = Analizador().analizar(entrada.tokens_para_parser())
    for error in resultado.errores:
        token = error.encontrado
        print(
            f"{ruta}:{token.linea}:{token.columna}: {error.mensaje}",
            file=sys.stderr,
        )
    if not resultado.correcto:
        return None
    tabla = TablaSimbolos()
    if mostrar_tabla:
        print("Cambios de la tabla de simbolos")
        tabla.al_cambiar = lambda cambio: imprimir_cambio_parcial(
            tabla, cambio)
    errores = verificar_semantica(resultado.arbol, tabla)
    if mostrar_tabla:
        print("\nTabla de simbolos final")
        print(tabla.a_texto(), end="")
    if reportar(errores, str(ruta), fuente):
        return None
    return resultado.arbol


def main():
    argumentos = argparse.ArgumentParser(
        description="Verificador semantico de Quantum Coffee"
    )
    argumentos.add_argument("archivo", type=Path)
    argumentos.add_argument(
        "--tabla", action="store_true",
        help="imprime los cambios de la tabla de simbolos y la tabla final")
    opciones = argumentos.parse_args()
    ruta = opciones.archivo
    try:
        fuente = ruta.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        argumentos.error(str(error))
    arbol = analizar_fuente(fuente, ruta, opciones.tabla)
    if arbol is None:
        return 1
    print(f"{ruta}: verificacion semantica correcta")
    print("ASA decorado en preorden")
    imprimir_preorden(arbol, con_semantica=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
