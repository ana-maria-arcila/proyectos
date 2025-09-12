import sympy as sym
import numpy as np

class hermite:
    """
    Clase para calcular polinomios de Hermite,
    usados en la solución del Oscilador Armónico Cuántico (OAC).
    """

    def __init__(self):
        """Inicializa la clase Hermite."""
        pass

    def solHermite(self, n, x):
        """
        Calcula el polinomio de Hermite de orden n evaluado en x.

        Parámetros
        ----------
        n : int
            Orden del polinomio de Hermite (corresponde al nivel de energía).
        x : numpy.ndarray
            Valores donde se evalúa el polinomio.

        Retorna
        -------
        H : numpy.ndarray
            Valores del polinomio de Hermite en los puntos de x.
        """
        z = sym.symbols('z')
        expPos = sym.exp(z ** 2)
        expNeg = sym.exp(-z ** 2)

        # Definición simbólica de Hermite
        solH = (-1) ** n * expPos * expNeg.diff(z, n)

        # Convertimos a función numérica
        f = sym.Lambda(z, solH)

        # Evaluación en los puntos x
        H = np.array([float(f(i)) for i in x])

        return H
