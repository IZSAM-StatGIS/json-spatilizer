import streamlit as st
import json
import requests
import pandas as pd

# st.set_page_config(layout="wide")
st.header('Convertitore servizio JSON plumber')
st.subheader('Inserire i parametri e scaricare il geojson')

col1, col2, col3 = st.columns(3)

with col1:
    from_date = st.date_input("Da:")
    
with col2:
    to_date = st.date_input("A:")
    
with col3:
    disease = st.number_input('ID Malattia:', min_value=0, step=1, value=16)

URL = "http://plumber-test.izs.intra:8080/FocolaiMalattiaPeriodo?SOSPETTO_FROM={0}&SOSPETTO_TO={1}&ID_MALATTIA={2}".format(from_date, to_date, disease)

qs_expander = st.expander('Query')
with qs_expander:
    st.write(URL)

# QUERY AL SERVIZIO PLUMBER E CONVERSIONE IN GEOJSON
try: 
    response = requests.get(URL)
    jsonResponse = response.json() 
    
    geojs={
        "type": "FeatureCollection",
        "features":[
            {
                "type":"Feature",
                "geometry": {
                "type":"Point",
                "coordinates":[d["LONGITUDINE"],d["LATITUDINE"]]
            },
                "properties":d,
            } for d in jsonResponse 
        ]  
    }
    
    j_expander = st.expander("GeoJSON Response")
    
    with j_expander:
        st.write(geojs)

    # VISUALIZZAZIONE SU MAPPA DELLA CONVERSIONE
    properties_list = [feature['properties'] for feature in geojs['features']]
    df = pd.DataFrame(properties_list)
    df.rename(columns={'LATITUDINE':'lat', 'LONGITUDINE':'lon'}, inplace=True)
    
    m_expander = st.expander("Map", expanded=True)
    with m_expander:
        st.map(df)

    st.download_button(
        label="Download GeoJSON",
        data=json.dumps(geojs),
        file_name='geodata.geojson',
        mime='application/json',
    )
    
except requests.exceptions.ConnectionError as connerr: 
    st.error("Errore di connessione: il servizio è disponibile solo all'interno della rete IZSAM!") 
    # st.write(errh.args[0]) 
 


