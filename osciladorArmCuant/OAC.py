import numpy as np
import matplotlib.pyplot as plt
import hermite as H
from scipy.special import factorial

class osciladorArmonicoCuantico:
    """
    Clase que modela el Oscilador Armónico Cuántico (OAC) 
    en una dimensión usando polinomios de Hermite.

    Métodos
    -------
    solucion(x, n):
        Calcula la función de onda al cuadrado (densidad de probabilidad)
        para un estado de energía n del OAC.
    Grafica(x, n):
        Grafica la densidad de probabilidad del OAC junto con
        la parábola del potencial armónico y el nivel de energía.
    """

    def __init__(self):
        """Inicializa el oscilador armónico cuántico."""
        pass

    def solucion(self, x, n):
        """
        Calcula la función de onda al cuadrado del OAC en el nivel n.

        Parámetros
        ----------
        x : numpy.ndarray
            Intervalo de posiciones en el cual se evalúa la función.
        n : int
            Número cuántico principal (nivel de energía).

        Retorna
        -------
        psi : numpy.ndarray
            Valores de la función de onda al cuadrado, desplazada
            según la energía del nivel n.
        """
        # Factor de normalización
        norm = 1 / np.sqrt(2 ** n * np.sqrt(np.pi) * factorial(n))

        ecHermite = H.hermite()
        solucionEc = ecHermite.solHermite(n, x)

        # Función de onda al cuadrado, desplazada por la energía (n + 1/2)
        psi = (norm * solucionEc * np.exp(-x ** 2 / 2)) ** 2 + (n + 1/2)

        return psi
    
    def Grafica(self, x, n):
        """
        Genera la gráfica de la densidad de probabilidad del OAC.

        Parámetros
        ----------
        x : numpy.ndarray
            Intervalo de posiciones en el cual se evalúa la función.
        n : int
            Número cuántico principal (nivel de energía).
        """
        # Línea horizontal de energía
        plt.axhline(n + 1/2, ls='--', alpha=0.3, c='k')

        # Potencial parabólico clásico
        plt.plot(x, x ** 2, c='k', alpha=0.3)

        # Función de onda al cuadrado
        plt.plot(x, self.solucion(x, n))
