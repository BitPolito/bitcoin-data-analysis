import streamlit as st
from PIL import Image
import requests
import base64

# ------------- Title of the page -------------
st.set_page_config(page_title='Bitcoin Blockchain live analysis', page_icon='₿', layout='wide')
# Title and bitcoin logos. a lot of them.
st.title('Analisi in diretta di Lightning Network - BitPolito')
bitcoin_logo = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/1200px-Bitcoin.svg.png'
bitpolito_logo = Image.open("bitpolito_logo.png")
col = st.columns(12)
logos = [bitcoin_logo, bitpolito_logo] * 6
for i in range(12):
    col[i].image(logos[i], width=50)

# TODO: add something useful
file_ = open("lightning.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
)