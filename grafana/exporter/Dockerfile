FROM python:3.9

ADD client.py .
ADD btc_conf.py .

RUN pip install prometheus_client python-bitcoinlib requests

CMD ["python", "./client.py"]