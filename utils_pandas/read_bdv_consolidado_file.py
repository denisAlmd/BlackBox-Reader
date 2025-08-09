import pandas as pd

def filtered_bdv_consolidado(file_path: str) -> pd.DataFrame:

    df = pd.read_excel(file_path, engine='openpyxl', header=2)
    
    df['Tempo'] = df['Tempo'].apply(lambda x: str(x).split(' ')[-1])
    df['Hora Chegada'] = df['Hora Chegada'].apply(lambda x: str(x).split(' ')[-1])
    df['Hora Saída'] = df['Hora Saída'].apply(lambda x: str(x).split(' ')[-1])
    df['Velocidade média'] = df["Km Rodado"] / df["Tempo"].apply(lambda x: convert_to_hours(x))
    
    negative_km_filter = df['Km Rodado'] < 0
    average_speed_filter = df['Velocidade média'] > 90
    
    if not negative_km_filter.any() and not average_speed_filter.any():
        return None    
    
    df['Status'] = ''
    
    df = df[negative_km_filter | average_speed_filter]
    
    df.loc[negative_km_filter, 'Status'] = 'Negative Odometer'
    df.loc[average_speed_filter, 'Status'] = 'High Average Speed'
    
    df['Velocidade média'] = df['Velocidade média'].apply(lambda x: f'{x:.2f} km/h' if x > 0 else 'N/A')    

    return df

def convert_to_hours(v:str):
    h, m, s = map(int, v.split(':'))
    return h + m / 60 + s / 3600