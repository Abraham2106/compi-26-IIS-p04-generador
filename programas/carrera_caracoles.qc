# Carrera de caracoles
# Configuracion
cafeteria grano META = 20;        # casillas para ganar
cafeteria grano PASO_MAXIMO = 3;  # avance maximo por turno
cafeteria grano SEMILLA = 7;      # cambiarla produce otra carrera

# Generador pseudoaleatorio: devuelve el numero que sigue al recibido
barista siguiente_azar(grano actual) {
    degustar (actual * 75 + 74) % 65537;
}

barista avance(grano azar) {
    degustar 1 + azar % PASO_MAXIMO;
}

# Dibuja la pista con el caracol "@" en su posicion
barista dibujar_pista(grano posicion) {
    granoMolido pista = "|";
    grano casilla = 0;
    chorreando (casilla <= META) {
        hierve (casilla == posicion) {
            pista = pista + "@";
        } enfria {
            pista = pista + "-";
        }
        casilla = casilla + 1;
    }
    degustar pista + "|";
}

barista mostrar_caracol(granoMolido nombre, grano posicion) {
    servir(dibujar_pista(posicion) + " " + nombre);
}

# Un caracol no puede pasarse de la meta
barista limitar(grano posicion) {
    hierve (posicion > META) {
        degustar META;
    }
    degustar posicion;
}

barista chorreador() {
    taza granoMolido caracoles = ["Turbo", "Moka", "Canela"];
    taza granoMolido ganadores = [];

    servir("=== Carrera de caracoles ===");
    recolar (granoMolido caracol en caracoles) {
        servir(caracol);
    }
    servir("Escriba el nombre del caracol al que apuesta:");
    granoMolido apuesta = leer();
    chorreando (Amargo caracoles.buscar(apuesta)) {
        servir("Ese caracol no corre. Intente de nuevo:");
        apuesta = leer();
    }

    grano turbo = 0;
    grano moka = 0;
    grano canela = 0;
    grano azar = SEMILLA;
    cafe terminada = ralo;

    chorreando (Amargo terminada) {
        azar = siguiente_azar(azar);
        turbo = limitar(turbo + avance(azar));
        azar = siguiente_azar(azar);
        moka = limitar(moka + avance(azar));
        azar = siguiente_azar(azar);
        canela = limitar(canela + avance(azar));

        servir("");
        mostrar_caracol("Turbo", turbo);
        mostrar_caracol("Moka", moka);
        mostrar_caracol("Canela", canela);

        terminada = turbo == META SinAzucar moka == META
            SinAzucar canela == META;
    }

    # Puede haber empate: todos los que llegaron en el mismo turno
    hierve (turbo == META) {
        ganadores.insertar("Turbo");
    }
    hierve (moka == META) {
        ganadores.insertar("Moka");
    }
    hierve (canela == META) {
        ganadores.insertar("Canela");
    }

    servir("");
    servir("Llegaron a la meta:");
    recolar (granoMolido ganador en ganadores) {
        servir(ganador);
    }
    hierve (ganadores.buscar(apuesta)) {
        servir("Ganaste la apuesta!");
    } enfria {
        servir("Perdiste la apuesta.");
    }
}