"""Transpila un archivo Quantum Coffee a Python."""

import argparse
import sys
from pathlib import Path

from generador import GeneradorPython
from parser.semantica.__main__ import analizar_fuente


def main():
    argumentos = argparse.ArgumentParser(description=__doc__)
    argumentos.add_argument("archivo", type=Path)
    ruta = argumentos.parse_args().archivo
    try:
        if ruta.suffix.lower() != ".qc":
            raise ValueError("se esperaba un archivo .qc")
        fuente = ruta.read_text(encoding="utf-8-sig")
        arbol = analizar_fuente(fuente, ruta)
        if arbol is None:
            return 1
        codigo = GeneradorPython().generar(arbol)
        ruta.with_suffix(".py").write_text(codigo, encoding="utf-8")
    except (OSError, ValueError) as error:
        print(f"{ruta}: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
