import streamlit as st
from PIL import Image
import requests
import base64
from bitdata.provider.mempool import MempoolProvider




# ------------- Title of the page -------------
st.set_page_config(page_title='Bitcoin Blockchain live analysis', page_icon='₿', layout='wide')
# Title and bitcoin logos. a lot of them.
st.title('Analisi in diretta di Lightning Network - BitPolito')
bitcoin_logo = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/1200px-Bitcoin.svg.png'
bitpolito_logo = Image.open("dashboard/bitpolito_logo.png")
col = st.columns(12)
logos = [bitcoin_logo, bitpolito_logo] * 6
for i in range(12):
    col[i].image(logos[i], width=50)




# Lightning Network Stats
ln_stats = MempoolProvider().get_lightning_stats()
# ln_sats: id=37293 added='2023-06-02T00:00:00.000Z' channel_count=70378 node_count=15700 total_capacity=536810389159 tor_nodes=11095 clearnet_nodes=2167 unannounced_nodes=1000 avg_capacity=7627531 avg_fee_rate=547 avg_base_fee_mtokens=850 med_capacity=2000000 med_fee_rate=40 med_base_fee_mtokens=125 clearnet_tor_nodes=1438

st.metric(label='Total number of nodes', value=ln_stats.node_count)
st.metric(label='Total number of channels', value=ln_stats.channel_count)
st.metric(label='Total capacity', value=ln_stats.total_capacity)
st.metric(label="Tor nodes", value=ln_stats.tor_nodes)
st.metric(label="Clearnet nodes", value=ln_stats.clearnet_nodes)
st.metric(label="Unannounced nodes", value=ln_stats.unannounced_nodes)
st.metric(label="Average capacity", value=ln_stats.avg_capacity)
st.metric(label="Average fee rate", value=ln_stats.avg_fee_rate)

    
st.header('Numero totale di nodi e canali')
st.subheader('Numero totale di nodi')
st.write('Il numero totale di nodi è pari a: ')
st.write('Il numero totale di canali è pari a: ')

# Lightning Graph

st.header("Lightning Network Graph")
# Add description
st.expander("""
Li
""")

# Add iframe graph
width = 800
height = 600
lngraph = f'<iframe allowfullscreen src="https://lnrouter.app/graph/embeded?height={height}px&width={width}px" height="{height}px" width="{width}px" style="overflow: hidden" scrolling="no" />'

with st.expander("Lightning Network Graph"):
    st.markdown(lngraph, unsafe_allow_html=True)
