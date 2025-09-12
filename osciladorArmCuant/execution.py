import hermite as H
import numpy as np
import matplotlib.pyplot as plt
import OAC
import json

# Leer parámetros de configuración desde un archivo JSON
with open('config.json', 'r') as archivo:
    datos = json.load(archivo)

# Niveles cuánticos a graficar
n = datos['n']

# Crear objeto de oscilador armónico cuántico
sol = OAC.osciladorArmonicoCuantico()

# Definir el rango de posiciones
x = np.linspace(-2, 2, 100)

# Graficar la función de onda al cuadrado para cada nivel
for i in range(len(n)):
    sol.Grafica(x, n[i])

# Guardar la gráfica en archivo
plt.savefig('GraficaOAC.jpg')
