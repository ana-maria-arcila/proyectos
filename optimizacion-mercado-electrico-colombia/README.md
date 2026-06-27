# optimizacion-mercado-electrico-colombia
27/06/2026

Notebooks y módulos Python que implementan un modelo simplificado de despacho económico para el Sistema Interconectado Nacional (SIN) de Colombia, usando datos abiertos de [SIMEM](https://www.simem.co).

## Descripción

El Centro Nacional de Despacho (CND), operado por XM, resuelve diariamente el problema de despacho económico: dado que hay que satisfacer una demanda D, ¿cuánto debe generar cada planta para minimizar el costo total del sistema?

Este proyecto implementa una versión simplificada de ese problema usando programación lineal (PuLP) y lo compara contra el despacho real de XM durante 2025.

## Datos

Todos los datos provienen de SIMEM (Sistema de Información del Mercado de Energía Mayorista), operado por XM:

| Dataset | ID | Descripción |
|---|---|---|
| Generación real y programada | E17D25 | Generación diaria por planta |
| Costo marginal redespacho | 03e35f | Precio horario del mercado |
| Demanda real | 9b0967 | Demanda diaria por agente |
| Aportes hídricos | 2bff14 | Aportes diarios por cuenca |
| Capacidad efectiva por planta | FADED0 | Capacidad instalada en kW |
| Precio de oferta despacho ideal | b1189f | Costo declarado por planta en COP/kWh |

## Metodología

El modelo minimiza el costo total de generación diaria:

**Costos por fuente (COP/kWh):**
| Fuente | Costo | Fuente del dato |
|---|---|---|
| Solar | 84 | Precio de oferta declarado al CND |
| Cogeneración | 30 | Estimado, no declaran precio al CND |
| Eólica | 75 | Estimado, no declaran precio al CND |
| Hidráulica | 331 | Precio de oferta declarado al CND |
| Térmica | 794 | Precio de oferta declarado al CND |

**Límites de generación:**
- Hidráulica, solar y eólica: limitadas a la generación real del día (refleja disponibilidad del recurso)
- Térmica y cogeneración: limitadas a la capacidad instalada del SIN

## Resultados principales

- El modelo sugiere consistentemente menos generación térmica que el despacho real de XM (~15-30 GWh/día menos)
- Se especula que diferencia se explica por restricciones operativas que el modelo no captura: contratos de disponibilidad, restricciones de red, gestión de embalses y exportaciones a Ecuador y Venezuela
- El ahorro teórico anual de seguir el despacho óptimo del modelo es de ~6 billones COP, atribuible principalmente a la sustitución de térmica por cogeneración
- 2025 fue un año con período seco pronunciado (enero–abril): los aportes hídricos estuvieron por debajo de la media histórica, la generación térmica aumentó significativamente y el costo marginal alcanzó picos de 1,000+ COP/kWh

## Limitaciones

- Costos de eólica y cogeneración son estimados, estas fuentes no declaran precio de oferta al CND
- El modelo no captura restricciones de red, contratos de disponibilidad ni exportaciones internacionales
- La capacidad de cogeneración disponible se asume constante, cuando en realidad depende de la temporada de cosecha (ingenios azucareros)
- Los costos de oferta declarados corresponden a junio 2026, no a 2025

## Estructura

optimizacion-mercado-electrico-colombia/

├── requirements.txt       # Librerías utilizdas

├── data_dlwd.py       # Descarga de datos vía API SIMEM

├── modelo.py          # Modelo de optimización (PuLP)

└── analisis.ipynb     # Exploración, resultados y visualizaciones

