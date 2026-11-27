barista chorreador() {
    taza granoMolido turnos = [];
    grano pendientes = 0;
    granoMolido opcion = "";
    chorreando (opcion != "4") {
        servir("1 Agregar | 2 Atender | 3 Consultar | 4 Salir");
        opcion = leer();
        hierve (opcion == "1") {
            servir("Nombre:");
            turnos.insertar(leer());
            pendientes = pendientes + 1;
        }
        hierve (opcion == "2") {
            hierve (pendientes > 0) {
                servir("Atendiendo a " + turnos.extraer(0));
                pendientes = pendientes - 1;
            } enfria {
                servir("No hay turnos pendientes");
            }
        }
        hierve (opcion == "3") {
            servir("Turnos pendientes:");
            servir(pendientes);
        }
    }
}
