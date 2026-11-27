"""Soporte cuántico que se copia a los programas que declaran qubits."""

from math import sqrt
from random import random

_estado = [1.0]


def _qubit():
    mascara = len(_estado)
    _estado.extend([0.0] * mascara)
    return mascara


def _puerta(puerta, a, b=None):
    if puerta == "Z":
        for i in range(len(_estado)):
            if i & a:
                _estado[i] *= -1
        return
    objetivo = b if puerta == "CNOT" else a
    for i in range(len(_estado)):
        if i & objetivo or (puerta == "CNOT" and not i & a):
            continue
        j = i | objetivo
        x, y = _estado[i], _estado[j]
        if puerta == "H":
            _estado[i], _estado[j] = (x + y) / sqrt(2), (x - y) / sqrt(2)
        else:
            _estado[i], _estado[j] = y, x


def _medir(qubit):
    pesos = [0.0, 0.0]
    for i, amplitud in enumerate(_estado):
        pesos[bool(i & qubit)] += amplitud ** 2
    resultado = not pesos[False] or random() * sum(pesos) < pesos[True]
    norma = sqrt(pesos[resultado])
    for i, amplitud in enumerate(_estado):
        _estado[i] = amplitud / norma if bool(i & qubit) == resultado else 0.0
    return resultado
