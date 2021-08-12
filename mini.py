from PIL import Image
import streamlit as st
import base64


sipe = Image.open('Sipe.jpeg')
rama = Image.open('Rama.jpeg')

file = open('last.gif', 'rb')
contents = file.read()
data_url = base64.b64encode(contents).decode("utf-8")
file.close()

audio_file = open('look.ogg', 'rb')
audio_bytes = audio_file.read()

st.title("Hello Sipe")

st.write("Selamat ulang tahun my sipe :heart:")
st.write("Sekarang klik play dulu hehe")
st.audio(audio_bytes, format='audio/ogg')

st.write("""
Makasih udah mau tetep sabar sama aku meskipun aku sering ngeselin.
Makasih udah selalu ada untuk aku sampe sekarang.

Semoga sipe bisa tetep seneng meskipun aku ga bisa ngasih sesuatu yang terlalu 'wah'.\n
Semoga sipe bisa terus jadi sipe yang lebih baik.\n
Semoga sipe bisa tetep seneng sama aku dan sabar kalau akunya ngeselin.\n
Semoga kita bisa terus bareng ya my sipe :heart:

Sekarang coba klik tombol di bawah
""")

btn_appear = None

if st.button("Pertama"):
    st.image(sipe, caption='My Sipe Miuw')
    st.write("""
    Aku suka foto sipe yang ini :kissing_heart:
    Sipe nya keliatan seneng hehehe.
    Aku suka kalau sipe seneng.
    """)

if st.button("Kedua"):
    st.write("""
    Bagaimanapun juga, aku adalah ama yang serius dan formal.
    Gambar di bawah ini adalah grafik yang menunjukan perasaan sayang aku ke sipe.
    """)

    st.line_chart({'data': [x for x in range(10)]})
    st.caption("Sebenernya ini maksudnya selalu meningkat gitu")

    st.write("""
    Tapi ternyata untuk gambar grafik yang lebih bagus rada susah dan aku bikin ini jam 8 tadi
    Maafin ga nyiapin sesuatu yang lebih serius :point_right::point_left:
    """)

if st.button("Ketiga"):
    st.write("Aku lagi liatin sipe lucu")
    st.image(rama, caption="Maapin foto aku ga senyum kaya kamu hehe")

    st.write("""
    Pokonya aku seneng sama sipe hehehe
    Aku pengen kita terus kaya gini dan lebih baik
    
    Makasihh hehe
    
    Loveyou sayang :heart::heart::heart:
    """)

if st.button("Keempat"):
    st.write("Ini yang terkahir hehe. Maapin aku asal satuin aja di internet :rolling_on_the_floor_laughing:")
    st.write("Tapi coba enjoy aja sambil dengerin lagunya")

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="kita">',
        unsafe_allow_html=True
    )

    st.write(":kissing_heart:")
