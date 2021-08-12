import pandas as pd
import streamlit as st
import pydeck as pdk
from pydeck.types import String

from util import bmkg_to_final


koordinat = pd.read_csv('koordinat.csv', delimiter=';')
coord = koordinat.set_index('stasiun')
list_nama = koordinat.stasiun.unique()

koor_dict = {}
for x in list_nama:
    koor_dict[x] = [coord.loc[x].lon, coord.loc[x].lat]


def add_coordinates(row):
    try:
        return koor_dict[row['stasiun']]
    except KeyError:
        return [6, 95]


df_2017 = pd.read_csv('dataset/laporan iklim harian/laporan_iklim_harian_2017.csv')

table = bmkg_to_final(df_2017)

table['singkat'] = table['stasiun'].str.replace('Stasiun', '')
table['singkat'] = table['singkat'].str.replace('Meteorologi', '')
table['singkat'] = table['singkat'].str.replace('Klimatologi', '')
table['singkat'] = table['singkat'].str.replace('Geofisika', '')
table['singkat'] = table['singkat'].str.replace('Maritim', '')

table['koordinat'] = table.apply(lambda row: add_coordinates(row), axis=1)

min_table = table.loc[table.tipe == 'min']
max_table = table.loc[table.tipe == 'max']

st.title("Peta Stasiun BMKG Indonesia")


month = st.sidebar.selectbox(
    "Bulan",
    ("Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober",
     "November", "Desember")
)

temperature_type = st.sidebar.radio(
    "Suhu",
    ("Min", "Max")
)

if temperature_type == "Min":
    data = min_table
else:
    data = max_table

if month == 'Januari':
    data['tanggal'] = data['t01']
    data['suhu'] = data['s01']
elif month == 'Februari':
    data['tanggal'] = data['t02']
    data['suhu'] = data['s02']
elif month == 'Maret':
    data['tanggal'] = data['t03']
    data['suhu'] = data['s03']
elif month == 'April':
    data['tanggal'] = data['t04']
    data['suhu'] = data['s04']
elif month == 'Mei':
    data['tanggal'] = data['t05']
    data['suhu'] = data['s05']
elif month == 'Juni':
    data['tanggal'] = data['t06']
    data['suhu'] = data['s06']
elif month == 'Juli':
    data['tanggal'] = data['t07']
    data['suhu'] = data['s07']
elif month == 'Agustus':
    data['tanggal'] = data['t08']
    data['suhu'] = data['s08']
elif month == 'September':
    data['tanggal'] = data['t09']
    data['suhu'] = data['s09']
elif month == 'Oktober':
    data['tanggal'] = data['t10']
    data['suhu'] = data['s10']
elif month == 'November':
    data['tanggal'] = data['t11']
    data['suhu'] = data['s11']
elif month == 'Desember':
    data['tanggal'] = data['t12']
    data['suhu'] = data['s12']


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
            data,
            pickable=True,
            get_position='koordinat',
            get_text='singkat',
            get_size=16,
            get_color=[0, 0, 0],
            get_angle=0,
            get_text_anchor=String("middle"),
            get_alignment_baseline=String("center")
        )
    ],
    tooltip={"text": "{stasiun}\n{tanggal}\n{suhu}"},
    map_style=pdk.map_styles.ROAD,
))
