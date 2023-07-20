# Raw version, should be edit to launch all in one command (bash script?)
- launch call.py (promethesu client) <br>
- start prometheus server and correctly bind config file (docker command --> docker run -d --name prometheusContainer -v \"$(pwd)/config/prometheus.yml":/etc/prometheus/prometheus.yml -p "9090:9090" prom/prometheus)<br>
- start grafana container (docker command --> docker run -d --name=grafanaContainer -p 3000:3000 grafana/grafana) <br>
- Connect to grafana istance and add prometheus as datasource <br>