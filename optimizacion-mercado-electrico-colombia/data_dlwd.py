import requests
import json
import pandas as pd

def get_simem_data(dataset_id, start_date, end_date):
    """
    Descarga datos de SIMEM via streaming y retorna un DataFrame.
    
    Args:
        dataset_id: ID del dataset (ej: 'E17D25')
        start_date: Fecha inicio 'YYYY-MM-DD'
        end_date: Fecha fin 'YYYY-MM-DD'
    
    Returns:
        DataFrame con los registros, o None si falla
    """
    url = f"https://www.simem.co/backend-files/api/datos-publicos?datasetId={dataset_id}&startDate={start_date}&endDate={end_date}"
    
    buffer = ""
    with requests.post(url, json=[], stream=True) as response:
        if response.status_code != 200:
            print(f"Error {response.status_code} para dataset {dataset_id}")
            return None
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                buffer += chunk.decode('utf-8')
    
    try:
        data = json.loads(buffer)
        df = pd.DataFrame(data)
        print(f"Dataset {dataset_id}: {df.shape[0]} registros, {df.shape[1]} columnas")
        return df
    except json.JSONDecodeError as e:
        print(f"Error parseando JSON: {e}")
        return None