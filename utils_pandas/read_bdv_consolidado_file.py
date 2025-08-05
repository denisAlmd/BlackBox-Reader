import pandas as pd

def check_negative_km(df: pd.DataFrame):
    """
    Checks for negative odometer values in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if negative odometer values are found, False otherwise.
    """

    df =  df["Km Rodado"].any() < 0

    if df:
        return df[df["Km Rodado"] < 0]
    return None

def convert_to_seconds(time_str: str) -> int:
    """
    Converts a time string in HH:MM:SS format to seconds.
    
    Args:
        time_str (str): Time string in HH:MM:SS format.
        
    Returns:
        int: Time in seconds.
    """
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def check_average_speed(df: pd.DataFrame) -> pd.DataFrame:
    """
    Checks for average speed anomalies in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        pd.DataFrame: A DataFrame containing rows with average speed anomalies.
    """

    # Calculate average speed
    df["Average Speed"] = df["Km Rodado"].apply(lambda x: x * 1000) / df["Tempo"].apply(lambda x: convert_to_seconds(x)) * 3.6  # Convert to km/h
    

    # Check for anomalies (e.g., unrealistic speeds)
    anomalies = df[(df["Average Speed"] > 90)]

    if not anomalies.empty:
        return anomalies

    return None

def read_bdv_consolidado_file(file_path: str) -> pd.DataFrame:
    """
    Reads a BDV consolidado file and returns a DataFrame.

    Args:
        file_path (str): The path to the BDV consolidado file.

    Returns:
        pd.DataFrame: A DataFrame containing the data from the BDV consolidado file.
    """

    df = pd.read_excel(file_path, engine='openpyxl', header=2)

    df['Tempo'] = pd.to_timedelta(df['Tempo']).dt.components.apply(
    lambda row: f"{int(row.hours):02}:{int(row.minutes):02}:{int(row.seconds):02}", axis=1)
    
    df['Hora Chegada'] = pd.to_timedelta(df['Hora Chegada']).dt.components.apply(
    lambda row: f"{int(row.hours):02}:{int(row.minutes):02}:{int(row.seconds):02}", axis=1)

    df['Hora Saída'] = pd.to_timedelta(df['Hora Saída']).dt.components.apply(
    lambda row: f"{int(row.hours):02}:{int(row.minutes):02}:{int(row.seconds):02}", axis=1)

    negative_km_df = check_negative_km(df)
    average_speed_df = check_average_speed(df)

    if negative_km_df is not None or average_speed_df is not None:
        final_df = pd.concat([negative_km_df, average_speed_df], ignore_index=True)
    else:
        final_df = None

    return final_df