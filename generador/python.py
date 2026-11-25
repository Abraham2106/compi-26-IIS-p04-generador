"""Emisión de expresiones Python a partir del ASA verificado."""

from parser.semantica.visitante import VisitanteASA

OPERADORES = {"ConAzucar": "and", "SinAzucar": "or", "Amargo": "not"}
LITERALES = {
    "FUERTE": "True", "RALO": "False", "DESCAFEINADO": "None",
    "SE_QUEMO_EL_CAFE": "NotImplemented",
}


class GeneradorPython(VisitanteASA):
    def visitar_generico(self, nodo):
        p = nodo.rango.inicio
        raise ValueError(
            f"{p.linea}:{p.columna}: nodo sin emisión {nodo.clase}"
        )

    def nombre(self, nodo):
        p = nodo.rango.inicio
        return f"qc_{nodo.atributos['nombre']}_{p.linea}_{p.columna}"

    def referencia(self, nodo, papel="nombre"):
        return self.nombre(nodo.semantica.definiciones[papel])

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
