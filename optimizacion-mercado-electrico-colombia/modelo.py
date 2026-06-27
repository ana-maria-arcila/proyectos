# modelo.py
import pulp
import pandas as pd

def calcular_costos(costo_por_planta):
    """Calcula costos promedio por tipo de generación."""
    costos = costo_por_planta.groupby('TipoGeneracion')['CostoOferta'].mean()
    return {
        'hidro':    costos['Hidraulica'],
        'termica':  costos['Termica'],
        'solar':    costos['Solar'],
        'eolica':   75,   # no declaran, costo operativo estimado
        'cogen':    30,   # no declaran, costo operativo estimado
    }

def calcular_capacidades(capacidad_max):
    """Calcula capacidad máxima diaria por tipo en kWh."""
    return capacidad_max.groupby('TipoGeneracion')['Valor'].sum() * 24

def despacho_optimo(fecha, df_master, costos, CAP):
    """
    Resuelve el despacho económico para una fecha dada.
    
    Args:
        fecha: string 'YYYY-MM-DD'
        df_master: DataFrame con datos diarios del sistema
        costos: dict con costos por tipo de fuente (COP/kWh)
        CAP: Series con capacidad máxima por tipo (kWh/día)
    
    Returns:
        dict con generación óptima por fuente y costo total
    """
    row = df_master[df_master['Fecha'] == pd.Timestamp(fecha)].iloc[0]
    demanda = row['DemandaTotal']

    prob = pulp.LpProblem(f"Despacho_{fecha}", pulp.LpMinimize)

    hidro   = pulp.LpVariable("Hidro",   0, row['Hidraulica'])
    termica = pulp.LpVariable("Termica", 0, CAP['Termica'])
    solar   = pulp.LpVariable("Solar",   0, row['Solar'])
    eolica  = pulp.LpVariable("Eolica",  0, row['Eolica'])
    cogen   = pulp.LpVariable("Cogen",   0, CAP['Cogenerador'])

    prob += (costos['hidro']   * hidro +
             costos['termica'] * termica +
             costos['solar']   * solar +
             costos['eolica']  * eolica +
             costos['cogen']   * cogen)

    prob += hidro + termica + solar + eolica + cogen >= demanda

    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    # Costo marginal = costo de la fuente más cara despachada
    if pulp.value(termica) > 0:
        costo_marginal = costos['termica']
    elif pulp.value(hidro) > 0:
        costo_marginal = costos['hidro']
    elif pulp.value(cogen) > 0:
        costo_marginal = costos['cogen']
    else:
        costo_marginal = costos['solar']

    return {
        'fecha':                 fecha,
        'status':                pulp.LpStatus[prob.status],
        'demanda_GWh':           demanda / 1e6,
        'hidro_GWh':             pulp.value(hidro)   / 1e6,
        'termica_GWh':           pulp.value(termica) / 1e6,
        'solar_GWh':             pulp.value(solar)   / 1e6,
        'eolica_GWh':            pulp.value(eolica)  / 1e6,
        'costo_total':           pulp.value(prob.objective),
        'costo_marginal_modelo': costo_marginal,
        'cogen_GWh': pulp.value(cogen) / 1e6,
    }

def correr_anio(df_master, costos, CAP):
    """Corre el modelo para todos los días del DataFrame."""
    resultados = []
    for fecha in df_master['Fecha']:
        r = despacho_optimo(fecha.strftime('%Y-%m-%d'), df_master, costos, CAP)
        resultados.append(r)
    return pd.DataFrame(resultados)