# Dashboard on Grafana
## Pipeline <br>
- exporter --> prometheus --> grafana <br>

## Usage
1) Edit btc_conf.py in exporter folder, mainly you should change: <br>
- RPC_USER = "Put_here_your_btc_server_username" <br>
- RPC_PASSWORD = "put_here_your_btc_server_password" <br>
- RPC_HOST = "localhost", here you should put the ip of your container (if docker is used) <br>
Others parameters should be ok but take anyway a look.<br>

2) In the compose file you probably should change the docker network on which your bitcoin core node is running. If you're using umbrel and your installation of btc core is done through umbrell app store you should already be ok, orherwise change the network to fit your needed.

3) Last step is to finally run docker-compose.yml
```
docker-compose up --build -d
```
As you can see in the compose file, exporter sends data on port 9000, prometheus server is on port 9090 and grafana on 11000. <br>
Compose file also contains a volume for grafana, so you can save your dashboards and data even if you restart the container (prometheus and exporter don't need a volume so far). <br>
To test if everything is working connect on port 11000 on your machine and you should see grafana login page. <br>

### Some info on client.py
Client.py is written in python, it's a simple script that connects to bitcoin core node and gets data from it. <br>
If you need debug information just set DEBUG = 1 and you'll see all the data that are fetched from bitcoin core. <br>
At the moment client.py rely on bitcoin core RPC, but it's possible to use bitcoin-cli instead, this feature is available in the code but not used, if needed just change BITCOIN_CLI = 1 and you'll use bitcoin-cli instead of RPC (warning: bitcoin-cli is slower than RPC and you should edit a little bit the code to make it working on your machine ex. right bitcoin-cli path). <br>