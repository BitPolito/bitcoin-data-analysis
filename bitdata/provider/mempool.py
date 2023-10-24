import requests
from pydantic import BaseModel


class LightningStats(BaseModel):
    id: int
    added: str
    channel_count: int
    node_count: int
    total_capacity: int
    tor_nodes: int
    clearnet_nodes: int
    unannounced_nodes: int
    avg_capacity: int
    avg_fee_rate: int
    avg_base_fee_mtokens: int
    med_capacity: int
    med_fee_rate: int
    med_base_fee_mtokens: int
    clearnet_tor_nodes: int


class MempoolProvider:
    def __init__(self) -> None:

        pass

    def get_lightning_stats(self):
        """Returns network-wide stats such as total number of channels and nodes, total capacity, and average/median fee figures."""

        url = "https://mempool.space/api/v1/lightning/statistics/latest"
        response = requests.get(url)
        result = self.parse_result(response)
        if not result:
            return None

        stats = result.get("latest", None)
        if not stats:
            return None

        try:
            return LightningStats(**stats)
        except Exception as e:
            print(e)
            return stats

    def parse_result(self, result):
        if result.status_code == 200:
            return result.json()
        else:
            return None


if __name__ == "__main__":
    mempool = MempoolProvider()
    stats = mempool.get_lightning_stats()
    print(stats)
