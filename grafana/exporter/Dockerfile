FROM python:3.9

ADD exporter/client.py .
ADD exporter/btc_conf.py .

RUN pip install prometheus_client python-bitcoinlib

CMD ["python", "./client.py"]