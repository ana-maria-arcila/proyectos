import numpy as np
import random
import matplotlib.pyplot as plt

class decaida:
    """
    Clase que modela el decaimiento radiactivo estocástico de Radio (Ra) a Actinio (Ac).

    Atributos
    ----------
    Nra : int
        Número inicial de núcleos de Radio.
    Nac : int
        Número inicial de núcleos de Actinio.
    tmedRa : float
        Vida media del Radio.
    tmedAc : float
        Vida media del Actinio.
    """

    def __init__(self, Nra, Nac, tmedRa, tmedAc):
        """
        Inicializa el sistema con los valores iniciales de núcleos y vidas medias.

        Parámetros
        ----------
        Nra : int
            Número inicial de núcleos de Radio.
        Nac : int
            Número inicial de núcleos de Actinio.
        tmedRa : float
            Vida media del Radio.
        tmedAc : float
            Vida media del Actinio.
        """
        self.Nra = Nra
        self.Nac = Nac
        self.tmedRa = tmedRa
        self.tmedAc = tmedAc
        
    def dec(self):
        """
        Simula el proceso de decaimiento radiactivo Ra → Ac mediante un método estocástico.

        En cada paso de tiempo, se calcula la probabilidad de decaimiento de 
        cada núcleo de Ra y Ac, actualizando las poblaciones en el tiempo.

        Retorna
        -------
        N1 : list
            Evolución temporal del número de núcleos de Radio.
        N2 : list
            Evolución temporal del número de núcleos de Actinio.
        t : numpy.ndarray
            Vector de tiempos de la simulación.
        """
        lambdaRa = np.log(2) / self.tmedRa
        N1 = [self.Nra]
        lambdaAc = np.log(2) / self.tmedAc
        N2 = [self.Nac]

        t = np.linspace(0, 120, 1000)
        dt = 120/1000

        for i in range(1, len(t)):
            # Probabilidades de desintegración en este intervalo de tiempo
            P1 = 1 - np.exp(-dt * lambdaRa)
            P2 = 1 - np.exp(-dt * lambdaAc)

            # Desintegración estocástica del Ra
            N_1 = 0
            for _ in range(int(N1[-1])):
                if random.random() < P1:
                    N_1 += 1
            N1.append(N1[-1] - N_1)

            # Desintegración estocástica del Ac
            N_2 = 0
            for _ in range(int(N2[-1])):
                if random.random() < P2:
                    N_2 += 1

            # El Ac se alimenta del decaimiento del Ra y decae a su vez
            N2.append(N_1 + (N2[-1] - N_2))

        return N1, N2, t

    def figPlot(self):
        """
        Genera la gráfica de la evolución temporal de los núcleos de Ra y Ac.

        Muestra la simulación del decaimiento Ra → Ac en función del tiempo.
        """
        N1, N2, t = self.dec()
        plt.plot(t, N1, label="Ra")
        plt.plot(t, N2, label="Ac")
        plt.xlabel("Tiempo")
        plt.ylabel("Número de núcleos")
        plt.legend()
        plt.title("Decaimiento radiactivo Ra → Ac")
        plt.show()
