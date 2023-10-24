import requests

class QuickNode:
    def __init__(self, api_url = "https://docs-demo.btc.quiknode.pro/"):
        self.api_url = api_url
        
    def decode_raw_transaction(self, raw_transaction_hex):
        headers = {"Content-Type": "application/json"}

        # JSON data to be sent in the POST request
        data = {
            "method": "decoderawtransaction",
            "params": [raw_transaction_hex]
        }

        try:
            response = requests.post(api_url, json=data, headers=headers)
            if response.status_code == 200:
                decoded_transaction = response.json()
                return decoded_transaction
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print("Error:", e)
            return None