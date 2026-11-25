# Generador de código de Quantum Coffee

Proyecto final del curso Compiladores e Intérpretes. Este repositorio parte de
la implementación integrada del scanner, parser, ASA y verificador semántico
de Quantum Coffee. La siguiente etapa es incorporar el generador de código.

La base actual valida identificadores y tipos, administra ámbitos y una tabla
de símbolos, infiere tipos de retorno y decora el ASA con referencias a las
declaraciones. El generador todavía no está implementado.

## Requisitos

- Python 3.10 o posterior.
- Ruff para ejecutar el análisis de estilo.

Ejecuta los comandos desde la raíz del repositorio. El proyecto no requiere
dependencias externas para correr el verificador.

## Uso

Verificar un programa `.qc` con la base semántica:

```bash
python -m parser.semantica parser/ejemplos_completos/07_ajustes.qc
```

Imprimir los cambios parciales y la tabla final de símbolos:

```bash
python -m parser.semantica parser/ejemplos_completos/07_ajustes.qc --tabla
```

El comando termina con código `0` si el programa pasa la verificación y con
`1` si encuentra errores léxicos, sintácticos o semánticos. Los diagnósticos
indican archivo, línea, columna y el fragmento de código cuando corresponde.

Para ejecutar solo el scanner o el parser:

```bash
python scanner/main.py parser/ejemplos_completos/07_ajustes.qc
python -m parser parser/ejemplos_completos/07_ajustes.qc
```

## Desarrollo y validación

Ejecutar las pruebas:

```bash
python -m unittest discover -s parser/verificacion -t . -v
```

Revisar el estilo:

```bash
python -m ruff check parser scanner
```

## Estructura

- `scanner/`: análisis léxico.
- `parser/`: análisis sintáctico, integración del ASA y ejemplos `.qc`.
- `parser/semantica/`: tabla de símbolos, verificación de identificadores,
  inferencia de tipos, diagnósticos e interfaz de línea de comandos.
- `parser/verificacion/`: pruebas automatizadas.
- `docs/Tabla_de_simbolos.md`: diseño e impresión de la tabla de símbolos.
- `docs/Errores_y_pruebas/Demostracion.md`: guía para demostrar el verificador.

## Inicio de la etapa de generación

La implementación del generador debe integrarse después de la verificación
semántica para consumir el ASA decorado. El formato de salida y las
instrucciones concretas de generación se definirán de acuerdo con la
especificación del proyecto final.

## Equipo

- Abraham Solano Parrales
- Andrés Baldi
- Justin Lacayo
- Miguel Darío Soto Badilla
- Tomás Blando
