"""Emisión de Python a partir del ASA verificado."""

from pathlib import Path

from parser.asa_impresion import recorrer_preorden
from parser.integracion import ClaseNodo
from parser.semantica.visitante import VisitanteASA

OPERADORES = {"ConAzucar": "and", "SinAzucar": "or", "Amargo": "not"}
LITERALES = {
    "FUERTE": "True", "RALO": "False", "DESCAFEINADO": "None",
    "SE_QUEMO_EL_CAFE": "NotImplemented",
}


class GeneradorPython(VisitanteASA):
    def generar(self, arbol):
        self.lineas = []
        self.nivel = 0
        nodos = recorrer_preorden(arbol)
        if any(n.clase == ClaseNodo.QUBIT for _, n in nodos):
            soporte = Path(__file__).with_name("cuantica.py")
            self.lineas.extend(soporte.read_text(encoding="utf-8").splitlines())
            self.lineas.extend(("", ""))
        self.visitar(arbol)
        return "\n".join(self.lineas) + "\n"

    def visitar_generico(self, nodo):
        p = nodo.rango.inicio
        raise ValueError(
            f"{p.linea}:{p.columna}: nodo sin emisión {nodo.clase}"
        )

    def emitir(self, linea):
        self.lineas.append("    " * self.nivel + linea)

    def nombre(self, nodo):
        p = nodo.rango.inicio
        return f"qc_{nodo.atributos['nombre']}_{p.linea}_{p.columna}"

    def referencia(self, nodo, papel="nombre"):
        return self.nombre(nodo.semantica.definiciones[papel])

    def visitar_programa(self, nodo):
        principal = nodo.hijos[-1]
        for hijo in nodo.hijos[:-1]:
            if hijo.clase == ClaseNodo.FUNCION:
                self.visitar(hijo)
        self.visitar(principal)
        self.emitir('if __name__ == "__main__":')
        self.nivel += 1
        for hijo in nodo.hijos[:-1]:
            if hijo.clase != ClaseNodo.FUNCION:
                self.visitar(hijo)
        self.emitir("qc_chorreador()")
        self.nivel -= 1

    def visitar_funcion(self, nodo):
        *parametros, bloque = nodo.hijos
        firma = ", ".join(map(self.nombre, parametros))
        self.funcion(self.nombre(nodo), firma, bloque)

    def visitar_principal(self, nodo):
        self.funcion("qc_chorreador", "", nodo.hijos[0])

    def funcion(self, nombre, firma, bloque):
        self.emitir(f"def {nombre}({firma}):")
        self.nivel += 1
        globales = set()
        for _, nodo in recorrer_preorden(bloque):
            if nodo.clase == ClaseNodo.ASIGNACION:
                destino = nodo.semantica.definiciones["nombre"]
                if destino.clase == ClaseNodo.GLOBAL:
                    globales.add(self.nombre(destino))
        if globales:
            self.emitir("global " + ", ".join(sorted(globales)))
        self.visitar(bloque)
        self.nivel -= 1
        self.lineas.extend(("", ""))

    def visitar_bloque(self, nodo):
        if not nodo.hijos:
            self.emitir("pass")
        for hijo in nodo.hijos:
            expresion = self.visitar(hijo)
            if expresion is not None:
                self.emitir(expresion)

    def bloque(self, cabecera, nodo):
        self.emitir(cabecera + ":")
        self.nivel += 1
        self.visitar(nodo)
        self.nivel -= 1

    def visitar_local(self, nodo):
        valor = self.visitar(nodo.hijos[0]) if nodo.hijos else "None"
        self.emitir(f"{self.nombre(nodo)} = {valor}")

    visitar_global = visitar_local

    def visitar_asignacion(self, nodo):
        self.emitir(f"{self.referencia(nodo)} = {self.visitar(nodo.hijos[0])}")

    def visitar_condicional(self, nodo):
        condicion, si, *resto = nodo.hijos
        self.bloque(f"if {self.visitar(condicion)}", si)
        if resto:
            self.bloque("else", resto[0])

    def visitar_mientras(self, nodo):
        condicion, cuerpo = nodo.hijos
        self.bloque(f"while {self.visitar(condicion)}", cuerpo)

    def visitar_para_cada(self, nodo):
        lista = self.referencia(nodo, "lista")
        self.bloque(f"for {self.nombre(nodo)} in {lista}", nodo.hijos[0])

    def visitar_retorno(self, nodo):
        valor = self.visitar(nodo.hijos[0]) if nodo.hijos else ""
        self.emitir(f"return {valor}".rstrip())

    def visitar_identificador(self, nodo):
        return self.referencia(nodo)

    def visitar_literal(self, nodo):
        categoria = nodo.atributos["categoria"]
        lexema = nodo.atributos["lexema"]
        if categoria == "CADENA":
            return repr(lexema[1:-1])
        if categoria == "ENTERO":
            return str(int(lexema))
        return LITERALES.get(categoria, lexema)

    def visitar_binaria(self, nodo):
        op = nodo.atributos["operador"]
        a, b = map(self.visitar, nodo.hijos)
        return f"({a} {OPERADORES.get(op, op)} {b})"

    def visitar_unaria(self, nodo):
        op = nodo.atributos["operador"]
        return f"({OPERADORES.get(op, op)} {self.visitar(nodo.hijos[0])})"

    def visitar_lista(self, nodo):
        return "[" + ", ".join(map(self.visitar, nodo.hijos)) + "]"

    def visitar_llamada(self, nodo):
        if "nombre" in nodo.semantica.definiciones:
            funcion = self.referencia(nodo)
        else:
            funcion = {"leer": "input", "servir": "print"}[
                nodo.atributos["nombre"]]
        return funcion + "(" + ", ".join(map(self.visitar, nodo.hijos)) + ")"

    def visitar_operacion_lista(self, nodo):
        lista = self.referencia(nodo, "receptor")
        valor = self.visitar(nodo.hijos[0])
        metodo = nodo.atributos["metodo"]
        if metodo == "buscar":
            return f"({valor} in {lista})"
        operacion = {"insertar": "append", "extraer": "pop"}[metodo]
        return f"{lista}.{operacion}({valor})"

    def visitar_qubit(self, nodo):
        self.emitir(f"{self.nombre(nodo)} = _qubit()")

    def visitar_compuerta(self, nodo):
        puerta = nodo.atributos["compuerta"]
        args = ", ".join(map(self.visitar, nodo.hijos))
        self.emitir(f"_puerta({puerta!r}, {args})")

    def visitar_medicion(self, nodo):
        return f"_medir({self.visitar(nodo.hijos[0])})"
