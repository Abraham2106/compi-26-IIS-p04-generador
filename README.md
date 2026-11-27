# Generador de código de Quantum Coffee

Proyecto final del curso Compiladores e Intérpretes. Este repositorio parte de
la implementación integrada del scanner, parser, ASA y verificador semántico
de Quantum Coffee. El generador traduce el ASA decorado a un archivo Python 3.8 o superior.

La base actual valida identificadores y tipos, administra ámbitos y una tabla
de símbolos, infiere tipos de retorno y decora el ASA con referencias a las
declaraciones. El visitante del generador traduce expresiones y operadores a Python.

## Requisitos

- Python 3.12 o posterior.
- Ruff para ejecutar el análisis de estilo.

Ejecuta los comandos desde la raíz del repositorio. El proyecto no requiere
dependencias externas para correr el verificador.

## Uso

Verificar un programa `.qc` con la base semántica:

```bash
python -m parser.semantica archivo.qc
```

Imprimir los cambios parciales y la tabla final de símbolos:

```bash
python -m parser.semantica archivo.qc --tabla
```

El comando termina con código `0` si el programa pasa la verificación y con
`1` si encuentra errores léxicos, sintácticos o semánticos. Los diagnósticos
indican archivo, línea, columna y el fragmento de código cuando corresponde.

Para ejecutar solo el scanner o el parser:

```bash
python scanner/main.py archivo.qc
python -m parser archivo.qc
```

## Desarrollo y validación

Ejecutar las pruebas:

```bash
python -m unittest discover -s parser/verificacion -t . -v
```

Revisar el estilo:

```bash
python -m ruff check generador parser scanner
```

## Estructura

- `scanner/`: análisis léxico.
- `parser/`: análisis sintáctico, integración del ASA.
- `parser/semantica/`: tabla de símbolos, verificación de identificadores,
  inferencia de tipos, diagnósticos e interfaz de línea de comandos.
- `parser/verificacion/`: pruebas automatizadas.
- `docs/Tabla_de_simbolos.md`: diseño e impresión de la tabla de símbolos.
- `docs/Errores_y_pruebas/Demostracion.md`: guía para demostrar el verificador.

## Ejecutar el gestor de turnos

```bash
python -m generador programas/turnos.qc
python programas/turnos.py
```

## Equipo

- Abraham Solano Parrales
- Andrés Baldi
- Justin Lacayo
- Miguel Darío Soto Badilla
- Tomás Blando
