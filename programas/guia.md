# Carrera de caracoles

Desde la raíz del repositorio, generá y ejecutá el programa.

```bash
python -m generador programas/carrera_caracoles.qc
python programas/carrera_caracoles.py
```

Escribí `Turbo`, `Moka` o `Canela` para elegir tu apuesta. El programa dibuja
la posición de cada caracol en cada turno y anuncia quién llegó a la meta.
En caso de empate, muestra a todos los ganadores de ese turno.

Para inspeccionar solo el ASA decorado, ejecutá
`python -m parser.semantica programas/carrera_caracoles.qc`.
