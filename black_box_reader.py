from utils_pandas.read_blackbox_file import read_blackbox_file as rbbf
import streamlit as st

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
    
blackbox_reader_tab, = st.tabs(["Blackbox Reader"])

with blackbox_reader_tab:   
    uploaded_file = st.file_uploader("Upload a black box file", type=['xlsx'], accept_multiple_files=True)    
    uploaded_file.sort(key=lambda x: x.name)
    if uploaded_file is not None:
        for file in uploaded_file:
            st.write(f'### Blackbox: {file.name.split(".")[0]}')
            with st.spinner("Processing..."):
                df, data = read_blackbox_file(file)
            content(df, data)