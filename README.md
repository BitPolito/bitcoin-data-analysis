# Bitcoin Data Analysis

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/your-username/bitcoin-data-analysis/blob/main/LICENSE)

## Overview

The Bitcoin Data Analysis is a Python library designed to facilitate the analysis of Bitcoin on-chain data and Lightning Network data. It provides various functionalities and data providers to retrieve, process, and analyze Bitcoin-related information.

The library consists of the following components:

- **bitdata**: This module contains different providers to fetch Bitcoin data and some functions to help analysis.
- **dashboard**: This folder contains a Streamlit web page for visualizing and interacting with the analyzed data.


## Data Dashboard

Webpage built with streamlit, that displays some live statistics about bitcoin network. Try it [here](https://bumblebee00-data-analysis-on-chain-kk5uep.streamlit.app/)


### Installation

There are different ways to install the library.

<!-- ### Pip

1. Install the library from PyPI:

```bash
    pip install bitdata
``` -->


Clone the repository:
   
```bash
    git clone https://github.com/BitPolito/bitcoin-data-analysis
    cd bitcoin-data-analysis
```

#### Docker
If you don't have Docker installed, you can follow the instructions [here](https://docs.docker.com/get-docker/).

Build and run the docker image with:

```bash
    make docker 
```
Access the [streamlit](https://streamlit.io/) web page in your browser at http://localhost:8501.

#### Poetry
If you don't have poetry installed, follow the instructions in the [official Poetry documentation](https://python-poetry.org/docs/#installation) to install Poetry for your operating system.


Install python libraries
```
    poetry install
```
### Config
Add your own configuration file in the root folder of the project. 
You can use the .env.example file as a template.

```bash
cp .env.example .env
# edit .env file with your configuration
nano .env
```

## BitData - Analysis

Some examples tools and script to analyze bitcoin data.

### Coinbase String Monitor 
This script analyze the coinbase of the last 10 blocks of the testnet, if it found the target string on the coinbase transaction will send a message in a telegram channel.
Will continue to analyze new blocks every 30 seconds.

- Change BOT_TOKEN and CHAT_ID in the .env file to enable the telegram bot
- The bot should be added to the channel as an administrator. The CHAT_ID is the chat of the bot with the channel.

```
    poetry run python -m bitdata.analysis.coinbase -n testnet -t "Stratum v2" -p 10
```

### BP/LNP Stats Dashboard
```
    poetry run streamlit run dashboard/On-chain.py
```

Access the [streamlit](https://streamlit.io/) web page in your browser at http://localhost:8501.


### Mining pool distribution

```bash
    poetry run python -m bitdata.analysis.mining
```

### Transactions per block
```bash
    poetry run python -m bitdata.analysis.addresses
```
  
### Taproot transaction count 
```bash
    poetry run python -m bitdata.analysis.taproot
```

## Contributing

Contributions to the Bitcoin Data Analysis Library are welcome! If you encounter any issues, have feature suggestions, or would like to contribute code, feel free to open an issue or submit a pull request.

<!-- Please ensure that your contributions align with the project's coding style and follow the guidelines specified in the CONTRIBUTING.md file. -->

## License

The Bitcoin Data Analysis Library is open source and released under the [MIT License](https://github.com/your-username/bitcoin-data-analysis/blob/main/LICENSE).


## Acknowledgements
We would like to acknowledge the following resources and libraries that have contributed to the development of this project:

[bitnodes.io](https://bitnodes.io/)
[blockchain.info](https://www.blockchain.info)
[bloackstream.info](https://blockstream.info)


