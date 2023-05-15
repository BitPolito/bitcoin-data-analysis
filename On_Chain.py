import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from datetime import datetime, timedelta
from PIL import Image
import matplotlib.pyplot as plt

# ------------- Title of the page -------------
st.set_page_config(page_title='Bitcoin Blockchain live analysis', page_icon='₿', layout='wide')
# Title and bitcoin logos. a lot of them.
st.title('Analisi in diretta di Bitcoin - BitPolito')
bitcoin_logo = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/1200px-Bitcoin.svg.png'
bitpolito_logo = Image.open("bitpolito_logo.png")
col = st.columns(12)
logos = [bitcoin_logo, bitpolito_logo] * 6
for i in range(12):
    col[i].image(logos[i], width=50)

TODO = """ TODO: personalize this
# Configure CSS styles
st.markdown('''
<style>
    #button-links {
        text-decoration:none; 
        background-color:#f7931a; 
        color:white; 
        padding:20px; 
        display:block;
        box-shadow: 2px 2px 2px #FFFFFF;
        margin-bottom: 10px;
    }
    /*center metric label*/
    [data-testid="stMetricLabel"] {
        justify-content: center;
    }

    /*center metric value*/
    [data-testid="stMetricValue"] {
        color: #F7931A;
    }

    [data-testid="metric-container"] {
        box-shadow: 2px 2px 2px #FFFFFF;
        border: 2px solid #f7931a;
        padding: 10px;
    }

    .css-z5fcl4 {
        padding-top: 36px;
        padding-bottom: 36px;
    }

    .css-1544g2n {
        padding-top: 36px;
    }
</style>''', unsafe_allow_html=True)"""

# ------------- Bitcoin Nodes -------------
# create two columns
col1, col2 = st.columns(2)
# ----- on the first column put a map of the world with all the bitcoin nodes
map_data = requests.get('https://bitnodes.io/api/v1/snapshots/latest/?field=coordinates')
col1.header("Nodi Bitcoin nel mondo")
map_data = pd.DataFrame(map_data.json()['coordinates'], columns=['lat', 'lon'])
col1.map(map_data, zoom=1, use_container_width=True)
st.write("Fonte: https://bitnodes.io/")

# ----- on the second column put some statistics about the nodes
col2.header("Statistiche sui nodi")
nodes_data = requests.get('https://bitnodes.io/api/v1/snapshots/latest/')
nodes_data = nodes_data.json()
# numbr of nodes
col2.write(f"Nodi totali: **{nodes_data['total_nodes']}**")
# top cities
cities = {}
for node in nodes_data['nodes'].values():
    if node[-3] not in cities:
        cities[node[-3]] = 1
    else:
        cities[node[-3]] += 1
# sort cities by number of nodes
cities = {k: v for k, v in sorted(cities.items(), key=lambda item: item[1], reverse=True)}
del cities[None]
# display top 10 cities in a bullet list
col2.write("Top 10 città per numero di nodi:")
for i, info in enumerate(list(cities)[:10]):
    city = info.split('/')[1].replace('_', ' ')
    continent = info.split('/')[0]
    col2.write(f"{i+1}) {city} ({continent}): **{cities[info]} nodi**")


# ------------- Date sidebar (for network data) -------------
st.header("Startistiche sulla rete Bitcoin")
# Define date range dropdown options
date_ranges = {
    "All": 365*20,
    "Last 7 Days": 7,
    "Last 30 Days": 30,
    "Last 90 Days": 90,
    "Last Year": 365,
    "Last 5 Years": 365*5
}
# Create a selectbox panel for date filters
date_range = st.selectbox("Date Range", options=list(date_ranges.keys()))
end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
start_date = end_date - timedelta(days=date_ranges[date_range]) 

# ------------- Load network data -------------
def get_blockchaincom_data(url, col):
    data = requests.get(url).json()
    print(data.keys())
    df = pd.DataFrame(data['values']).rename(columns={"x":"Date","y":col})
    df['Date'] = pd.to_datetime(df['Date'], unit='s')
    df = df.sort_values(by="Date", ascending=False)
    return df 

@st.cache_data
def load_heavy_data():
    # Get historical BTC address data from Blockchain.com
    addr_url = 'https://api.blockchain.info/charts/n-unique-addresses?timespan=all&format=json'
    addr_df = get_blockchaincom_data(addr_url, "Addresses")

    # Get historical BTC transaction data from Blockchain.com
    tx_url = 'https://api.blockchain.info/charts/n-transactions?timespan=all&format=json'
    tx_df = get_blockchaincom_data(tx_url, "Transactions")


    # Get historical BTC hash rate data from Blockchain.com
    hs_url = 'https://api.blockchain.info/charts/hash-rate?timespan=all&format=json'
    hs_df = get_blockchaincom_data(hs_url, "Hash")

    # Get latest and second to last block data from Blockchain.com
    lastblock = requests.get('https://blockchain.info/latestblock').json()
    second_to_last_block = requests.get(f'https://blockchain.info/block-height/{lastblock["height"]-1}?format=json').json()


    return addr_df, tx_df, hs_df, lastblock, second_to_last_block

addr_df, tx_df, hash_df, lastblock, second_to_last_block = load_heavy_data()
addr_df = addr_df.loc[(addr_df['Date'] >= pd.Timestamp(start_date)) & (addr_df['Date'] <= pd.Timestamp(end_date))]
tx_df = tx_df.loc[(tx_df['Date'] >= pd.Timestamp(start_date)) & (tx_df['Date'] <= pd.Timestamp(end_date))]
hash_df = hash_df.loc[(hash_df['Date'] >= pd.Timestamp(start_date)) & (hash_df['Date'] <= pd.Timestamp(end_date))]


# ------------- Display network data in charts and metrics -------------
col1, col2 = st.columns(2)
# Create a line chart of hash rate
with col1:
    chart_hash = px.line(hash_df, x='Date', y='Hash', title='Hash rate totale', color_discrete_sequence=['#071CD8'])
    chart_hash.update_layout(yaxis_title='Hash rate Hash/s')
    st.plotly_chart(chart_hash, use_container_width=True)
# Create some other values
with col2:
    # metric for current hashrate
    current_hash = round(hash_df.iloc[0]['Hash']/10**9, 2)
    delta = round((hash_df.iloc[0]['Hash'] - hash_df.iloc[1]['Hash'])/10**9, 2)
    col2.metric(label="Hash rate attuale", value=f'{current_hash} TH/s', delta=f'{delta} TH/s')
    st.divider()
    # metric for current fees
    st.write("Commissioni (in sat/vB) per includere una transazione in ...")
    fees = requests.get('https://blockstream.info/api/fee-estimates').json()
    col2_1, col2_2, col2_3 = st.columns(3)
    col2_1.metric("1 blocco", f"{fees['1']:0.1f}")
    col2_2.metric("6 blocchi", f"{fees['6']:0.1f}")
    col2_3.metric("18 blocchi", f"{fees['18']:0.1f}")
    st.divider()
    # metric for lastest block time
    time_since_last_block = datetime.now() - datetime.fromtimestamp(lastblock['time'])
    last_block_minimg_time = datetime.fromtimestamp(lastblock['time']) - datetime.fromtimestamp(second_to_last_block['blocks'][0]['time'])
    m = '-' if last_block_minimg_time.seconds > 10*60 else ''
    
    col2.metric("Ultimo blocco minato ",
        f'{time_since_last_block.seconds//60} minuti e {time_since_last_block.seconds%60} seccondi fa',
        f"{m}in {last_block_minimg_time.seconds//60} minuti e {last_block_minimg_time.seconds%60} secondi",)
    st.divider()

# ------------- Display pools data in charts -------------
pools = requests.get('https://api.blockchain.info/pools?timespan=7days').json()
# sort json based on values
pools = {k: v for k, v in sorted(pools.items(), key=lambda item: item[1], reverse=True)}
# Extract the top 9 keys and values, and group all the others in a single key
sizes = list(pools.values())[:9]
labels = list(pools.keys())[:9]
sizes.append(sum(list(pools.values())[9:]))
labels.append('Others')

explode = [0.2 if k == 'Unknown' else 0 for k in labels]
colors = ['#FFC300', '#0080FF', '#FF0000', '#00BFFF', '#FF4D4D', '#0052CC', '#800000', '#FF9500', '#FFEA00', '#4B0082']
hatches = ['oo', 'o', '.', 'OO', 'xx', '-', '..', 'x', 'O']

fig1, ax1 = plt.subplots(figsize=(2, 2))
ax1.pie(sizes, autopct='%1.1f%%', pctdistance=1.25, explode=explode, colors=colors, hatch=hatches, textprops={'fontsize': 6})
ax1.legend(labels, loc='center left', bbox_to_anchor=(1.25, 0.5), fontsize=6)
st.pyplot(fig1, use_container_width=False)

# ------------- Display address and transaction data in graphs -------------
col1, col2 = st.columns(2)
# Create a line chart of daily addresses
with col1:
    chart_txn = px.line(tx_df, x='Date', y='Transactions', title='Transazioni giornaliere', color_discrete_sequence=['#F7931A'])
    chart_txn.update_layout(yaxis_title='Transactions')
    st.plotly_chart(chart_txn, use_container_width=True)
# Create a line chart of daily transactions
with col2:
    chart_addr = px.line(addr_df, x='Date', y='Addresses', title='Indirizzi attivi giornalieri', color_discrete_sequence=['#F7931A'])
    chart_addr.update_layout(yaxis_title='Active Addresses')
    st.plotly_chart(chart_addr, use_container_width=True)

st.write("Fonte: https://www.blockchain.info")
st.write("Fonte: https://blockstream.info")

preference = st.sidebar.radio(
    "Cosa preferisci?",
    ('-seleziona-', 'Bitcoin', 'Fiat'))

if preference == 'Bitcoin':
    st.balloons()
elif preference == 'Fiat':
    st.snow()