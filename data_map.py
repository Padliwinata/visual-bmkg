import pandas as pd
import streamlit as st
import pydeck as pdk
from pydeck.types import String

from util import bmkg_to_final


df = pd.read_csv('koordinat.csv', delimiter=';')
df = df.astype({'lat': float, 'lon': float})

df['singkat'] = df['stasiun'].str.replace('Stasiun', '')
df['singkat'] = df['singkat'].str.replace('Meteorologi', '')
df['singkat'] = df['singkat'].str.replace('Klimatologi', '')
df['singkat'] = df['singkat'].str.replace('Geofisika', '')
df['singkat'] = df['singkat'].str.replace('Maritim', '')

raw = pd.read_csv('dataset/laporan iklim harian/laporan_iklim_harian_2017.csv')
data = bmkg_to_final(raw)

st.title("Peta Stasiun BMKG Indonesia")


month = st.sidebar.selectbox(
    "Bulan",
    ("Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober",
     "November", "Desember")
)

# if month == 'Januari':
#     df['suhu_min'] = data[[]]


st.pydeck_chart(pdk.Deck(
    # map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=-4.449664376712999,
        longitude=119.80721106816641,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'TextLayer',
            df,
            pickable=True,
            get_position='[lon, lat]',
            get_text='singkat',
            get_size=16,
            get_color=[0, 0, 0],
            get_angle=0,
            get_text_anchor=String("middle"),
            get_alignment_baseline=String("center")
        )
    ],
    tooltip={"text": "{stasiun}"},
    map_style=pdk.map_styles.ROAD,
))
