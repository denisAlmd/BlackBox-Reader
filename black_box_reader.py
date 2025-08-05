from utils_pandas.read_blackbox_file import read_blackbox_file as rbbf
from utils_pandas.read_trip_blackbox import read_trip_blackbox as rtb
from utils_pandas.read_bdv_consolidado_file import read_bdv_consolidado_file as rbcf
import streamlit as st

from utils_pandas.read_trip_blackbox import read_trip_blackbox

st.set_page_config(
    page_title="File Reader",
    page_icon=":book:",
    layout="wide",
    
)
st.title("Blackbox Reader V1.0")
st.markdown("""
This is a simple tool to read and analyze black box data.
""")

@st.cache_data(show_spinner=False)
def read_blackbox_file(file_buffer):
    df, data = rbbf(file_buffer)
    return df, data

@st.cache_data(show_spinner=False)
def read_trip_blackbox(file_buffer, trip_start_time, trip_end_time):
    df = rtb(file_buffer, trip_start_time, trip_end_time)
    return df

def content(df,data):
    st.write("Blackbox's start and end.")
    st.dataframe(df)

    st.write(f'Initial and final odometer: {df["Odômetro"].iloc[0]:.2f} - {df["Odômetro"].iloc[-1]:.2f}')
    st.write(f'Distance traveled: {df["Odômetro"].iloc[-1] - df["Odômetro"].iloc[0]:.2f} km')
    if data['negative_odometer']:
        st.warning("Negative odometer detected!")
        
    st.write(f"Total rows: {data['rows']}")    
    if data['rows'] > 86400:
        st.warning("The file contains more than 86400 rows, the file is corrupted.")
        
    if data['average_speed'] is not None:
        st.write(f"Average speed: {data['average_speed']:.2f} km/h")
        
    if data['Tempo_duplicado'] is not None:
        st.warning('Duplicated Tempo values detected! The file is corrupted.')
        st.write('Some examples of duplicate "times" in the file:')
        st.dataframe(data['Tempo_duplicado'])
    
    # st.write("Data Summary:")
    # st.json(data)
    
    st.markdown("---")

blackbox_reader_tab, trip_blackbox_reader, bdv_consolidado_reader = st.tabs(["Blackbox Reader", "Trip Blackbox Reader", "BDV Consolidado Reader"])

with bdv_consolidado_reader:   
    uploaded_file = st.file_uploader("Upload a BDV consolidado file", type=['xlsx'], accept_multiple_files=False)    
    if uploaded_file is not None:
        st.write(f'### BDV Consolidado: {uploaded_file.name.split(".")[0]}')
        with st.spinner("Processing..."):
            df = rbcf(uploaded_file)
        if df is not None:
            st.write("Data with anomalies:")
            st.dataframe(df[['Data', "Organização",'Placa', 'Itinerários','Hora Saída', 'Hora Chegada', 'Tempo', 'Km Saída', 'Km Chegada', "Km Rodado", 'Matrícula', "Average Speed"]])
        else:
            st.error("No data corrupted in the file.")
        st.markdown("---")

with blackbox_reader_tab:   
    uploaded_file = st.file_uploader("Upload a black box file", type=['xlsx'], accept_multiple_files=True)    
    uploaded_file.sort(key=lambda x: x.name)
    if uploaded_file is not None:
        for file in uploaded_file:
            st.write(f'### Blackbox: {file.name.split(".")[0]}')
            with st.spinner("Processing..."):
                df, data = read_blackbox_file(file)
            content(df, data)

with trip_blackbox_reader:   
    max_files = 2
    start_trip = st.text_input('Digite o Tempo de início da viagem (formato: HH:MM:SS)', key='trip_start_time' , value='23:50:00')
    end_trip = st.text_input('Digite o Tempo de fim da viagem (formato: HH:MM:SS)', key='trip_end_time', value='23:59:59')
    uploaded_file = st.file_uploader("Upload a trip blackbox file", type=['xlsx'], accept_multiple_files=True, )
    if len(uploaded_file) > max_files:
        st.warning(f"You can only upload up to {max_files} files at a time.")
    else:           
        uploaded_file.sort(key=lambda x: x.name)
        if uploaded_file is not None and len(uploaded_file) == 1:
            st.write(f'### Trip Info Blackbox: {uploaded_file[0].name.split(".")[0]}')
            with st.spinner("Processing..."):
                df = read_trip_blackbox(uploaded_file[0], start_trip, end_trip)
            st.dataframe(df)
            km_rodado = df["Odômetro"].iloc[-1] - df["Odômetro"].iloc[0]
            st.write(f'Km rodado da viagem: {km_rodado:.2f} km')
            st.markdown("---")
        elif uploaded_file is not None and len(uploaded_file) == 2:
            st.write(f'### Trip Info Blackbox: {uploaded_file[0].name.split(".")[0]}')
            end_trip_aux = '23:59:59'
            with st.spinner("Processing..."):
                df = read_trip_blackbox(uploaded_file[0], start_trip, end_trip_aux)
            st.dataframe(df)
            km_rodado_trecho1 = df["Odômetro"].iloc[-1] - df["Odômetro"].iloc[0]
            st.write(f'Km rodado do primeiro trecho: {km_rodado_trecho1:.2f} km')

            st.write(f'### Trip Info Blackbox: {uploaded_file[1].name.split(".")[0]}')
            start_trip = '00:00:00'
            with st.spinner("Processing..."):
                df2 = read_trip_blackbox(uploaded_file[1], start_trip, end_trip)
            st.dataframe(df2)
            km_rodado_trecho2 = df2["Odômetro"].iloc[-1] - df2["Odômetro"].iloc[0]
            st.write(f'Km rodado do segundo trecho: {km_rodado_trecho2:.2f} km')
            st.write(f'Total Km rodado: {km_rodado_trecho1 + km_rodado_trecho2:.2f} km')
            st.markdown("---")
