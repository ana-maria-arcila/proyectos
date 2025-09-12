from decaimiento import decaida

if __name__ == '__main__':
    N1 = 5000      # Número inicial de núcleos de Radio (Ra)
    N2 = 0         # Número inicial de núcleos de Actinio (Ac)
    tmedRa = 14.8  # Vida media del Ra
    tmedAc = 10.8  # Vida media del Ac

    # Se crea un objeto de la clase 'decaida' con los parámetros iniciales
    dec1 = decaida(N1, N2, tmedRa, tmedAc)

    # Se ejecuta la simulación y se grafican los resultados
    dec1.figPlot()
