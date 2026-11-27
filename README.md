# Generador de código de Quantum Coffee

Proyecto final del curso Compiladores e Intérpretes. El transpilador convierte
programas Quantum Coffee (`.qc`) en archivos Python ejecutables. Integra el
scanner, el parser y el verificador semántico. El generador usa el patrón
Visitante para recorrer el árbol de sintaxis abstracta (ASA) decorado y emitir
código que respeta los tipos, las referencias y los ámbitos del programa.

La traducción incluye expresiones, declaraciones, asignaciones, funciones,
control de flujo, listas y entrada y salida por consola. Los programas con
qubits incorporan un simulador de compuertas y medición en el archivo generado.

## Requisitos

- Python 3.12 o posterior para ejecutar el transpilador.
- Python 3.8 o posterior para ejecutar el archivo generado.
- Ruff para la revisión de estilo durante el desarrollo.

El transpilador y los archivos generados usan la biblioteca estándar de Python.
Ejecutá los comandos desde la raíz del repositorio.

## Transpilar y ejecutar

```bash
python -m generador programas/carrera_caracoles.qc
python programas/carrera_caracoles.py
```

El comando escribe el `.py` junto al `.qc`. Si hay errores léxicos, sintácticos
o semánticos, muestra los diagnósticos y termina con código `1` antes de
escribir el archivo.

En la carrera podés apostar por Turbo, Moka o Canela y seguir sus avances hasta
la meta. [Guía de la carrera](programas/guia.md)

También podés ejecutar el gestor de turnos, que permite agregar un nombre,
atender a la siguiente persona y consultar cuántos turnos quedan.

```bash
python -m generador programas/turnos.qc
python programas/turnos.py
```

## Ejecutar las etapas por separado

```bash
python scanner/main.py archivo.qc
python -m parser archivo.qc
python -m parser.semantica archivo.qc
python -m parser.semantica archivo.qc --tabla
```

La opción `--tabla` muestra los cambios de la tabla de símbolos durante la
verificación y su estado final.

## Pruebas y estilo

```bash
python -m unittest discover -s parser/verificacion -t .
python -m ruff check generador parser scanner
```

Las pruebas de extremo a extremo transpilan y ejecutan los ocho ejemplos del
verificador. También comprueban diagnósticos, ámbitos, operaciones cuánticas y
el gestor de turnos. Por defecto ejecutan el código generado con el mismo
intérprete que corre las pruebas. Definí `QC_PYTHON_DESTINO` con la ruta a un
intérprete de Python 3.8 para repetir la prueba de compatibilidad.

## Estructura

- [scanner/](scanner/) contiene el análisis léxico.
- [parser/](parser/) contiene el análisis sintáctico y la construcción del ASA.
- [parser/semantica/](parser/semantica/) contiene el verificador y la tabla de símbolos.
- [generador/](generador/) contiene el visitante que emite Python y el soporte cuántico.
- [programas/](programas/) contiene la carrera de caracoles y el gestor de turnos.
- [parser/verificacion/](parser/verificacion/) contiene las pruebas automatizadas.

## Equipo

- Abraham Solano Parrales
- Andrés Baldi
- Justin Lacayo
- Miguel Darío Soto Badilla
- Tomás Blando
