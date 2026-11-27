"""Pruebas de extremo a extremo del transpilador."""

import ast
import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

RAIZ = Path(__file__).resolve().parents[2]
PYTHON_DESTINO = os.getenv("QC_PYTHON_DESTINO", sys.executable)


class TestGenerador(unittest.TestCase):
    def setUp(self):
        temporal = TemporaryDirectory()
        self.addCleanup(temporal.cleanup)
        self.fuente = Path(temporal.name) / "programa.qc"
        self.salida = self.fuente.with_suffix(".py")

    def transpilar(self, fuente):
        self.fuente.write_text(fuente, encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-m", "generador", str(self.fuente)],
            cwd=RAIZ, capture_output=True, text=True, timeout=10,
        )

    def ejecutar(self, fuente, entrada=""):
        resultado = self.transpilar(fuente)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        ast.parse(self.salida.read_text(encoding="utf-8"), feature_version=8)
        resultado = subprocess.run(
            [PYTHON_DESTINO, str(self.salida)],
            input=entrada, capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        return resultado.stdout.splitlines()

    def test_ejemplos_del_verificador(self):
        salidas = [
            ["682.5"],
            ["Orden lista para: Don Juan", "Bebida: Capuchino doble"],
            ["Agua al punto ideal para chorrear"],
            ["Bebida servida al cliente:", "Espresso",
             "Restante en el menu:", "Americano", "Latte"],
            ["Alerta critica: Hay que tostar mas cafe urgente"],
            None,
            ["Hola Ada", "[]", "5", "5", "5"],
            ["listo"],
        ]
        ejemplos = sorted((RAIZ / "parser/ejemplos_completos").glob("*.qc"))
        self.assertEqual(len(ejemplos), len(salidas))
        for archivo, esperado in zip(ejemplos, salidas):
            with self.subTest(archivo=archivo.name):
                salida = self.ejecutar(archivo.read_text("utf-8"), "Ada\n")
                if esperado is None:
                    self.assertIn(salida, (["True"], ["False"]))
                else:
                    self.assertEqual(salida, esperado)

    def test_errores_preservan_python_previo(self):
        carpeta = RAIZ / "parser/ejemplos_semanticos"
        fuentes = {p.name: p.read_text("utf-8") for p in carpeta.glob("*.qc")}
        fuentes.update(lexico="@",
                       sintaxis="barista chorreador() { grano x = ; }")
        self.salida.write_text("# previo\n", encoding="utf-8")
        for nombre, fuente in fuentes.items():
            with self.subTest(caso=nombre):
                resultado = self.transpilar(fuente)
                self.assertEqual(resultado.returncode, 1, resultado.stderr)
                self.assertIn(str(self.fuente), resultado.stderr)
                self.assertEqual(self.salida.read_text(), "# previo\n")

    def test_ambitos_y_llamada_adelantada(self):
        fuente = """cafeteria grano x = 1;
        barista cambiar() { x = siguiente(); }
        barista siguiente() { degustar 3; }
        barista chorreador() {
            cambiar();
            hierve (fuerte) { grano x = 2; servir(x); }
            servir(x);
        }"""
        self.assertEqual(self.ejecutar(fuente), ["2", "3"])

    def test_medicion_y_entrelazamiento(self):
        fuente = """barista chorreador() {
            qubit a; qubit b; qubit c;
            X(c); servir(medir(c));
            H(a); H(a); servir(medir(a));
            H(a); CNOT(a, b);
            servir(medir(a)); servir(medir(b));
        }"""
        salida = self.ejecutar(fuente)
        self.assertEqual(salida[:2], ["True", "False"])
        self.assertEqual(len(salida), 4)
        self.assertEqual(salida[2], salida[3])

    def test_turnos(self):
        fuente = (RAIZ / "programas/turnos.qc").read_text("utf-8")
        salida = self.ejecutar(fuente, "2\n1\nAna\n1\nLuis\n2\n3\n4\n")
        self.assertIn("No hay turnos pendientes", salida)
        self.assertIn("Atendiendo a Ana", salida)
        indice = salida.index("Turnos pendientes:")
        self.assertEqual(salida[indice + 1], "1")
