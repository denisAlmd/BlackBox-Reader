import pandas as pd

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

def read_blackbox_file (file_buffer):
    """
    Reads a blackbox file and returns a DataFrame.
    
    Parameters:
    - file_buffer: A file-like object or path to the blackbox file.
    - **kwargs: Additional keyword arguments to pass to pandas read_csv.
    
    Returns:
    - DataFrame containing the data from the blackbox file.
    """    
    # Read the blackbox file using pandas
    df = pd.read_excel(file_buffer, header=3, engine='openpyxl')
    
    data = {}
    
    rows = len(df)
    data['rows'] = rows
    
    max_odometer = df['Odômetro'].max()
    min_odometer = df['Odômetro'].min()
    data['negative_odometer'] =  max_odometer < min_odometer
    
    average_speed = check_average_speed(max_odometer, min_odometer, rows)
    data['average_speed'] = average_speed
   
    data['Tempo_duplicado'] = df['Tempo'].duplicated().any()
    data['Tempo_duplicado'] = df[df['Tempo'].duplicated(keep=False)].head(6) if data['Tempo_duplicado'] else None
    
    df_filtered = linhas_tempo_min_max(df)

    return df_filtered, data

def linhas_tempo_min_max(df):
    tempo_min = df['Tempo'].min()
    tempo_max = df['Tempo'].max()
    df_min = df[df['Tempo'] == tempo_min]
    df_max = df[df['Tempo'] == tempo_max]
    return pd.concat([df_min, df_max])

def check_average_speed(max_odometer, min_odometer, rows):
    """
    Checks if the average speed is within a reasonable range.
    """
    average_speed = (max_odometer - min_odometer) * 1000 / rows * 3.6
    return average_speed if average_speed > 0 and average_speed >= 90 else None  # Assuming a reasonable speed range