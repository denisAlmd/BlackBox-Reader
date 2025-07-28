import pandas as pd

def read_trip_blackbox(file_buffer, trip_start_time, trip_end_time) -> pd.DataFrame:
    df = pd.read_excel(file_buffer, header=3, engine='openpyxl')
    df = get_trip_data(df, trip_start_time, trip_end_time)
    return df

def get_trip_data(df, trip_start_time, trip_end_time):
    start_trip_df = df[df['Tempo'] == trip_start_time]
    end_trip_df = df[df['Tempo'] == trip_end_time]
    filtered_df = pd.concat([start_trip_df, end_trip_df])
    return filtered_df