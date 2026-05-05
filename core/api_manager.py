import requests
from PyQt6.QtCore import QThread, pyqtSignal

class PoolApiThread(QThread):
    stats_updated = pyqtSignal(dict)

    def __init__(self, wallet: str, pool: str):
        super().__init__()
        self.wallet = wallet
        self.pool = pool.lower()

    def run(self):
        if not self.wallet or not self.pool: 
            return
            
        try:
            unpaid = 0.0
            total_paid = 0.0
            
            if "2miners.com" in self.pool:
                url = f"https://xmr.2miners.com/api/accounts/{self.wallet}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    stats = data.get("stats", {})
                    unpaid = stats.get("balance", 0) / 1000000000000
                    total_paid = stats.get("paid", 0) / 1000000000000

            elif "moneroocean.stream" in self.pool or "c3pool.com" in self.pool:
                domain = "moneroocean.stream" if "moneroocean" in self.pool else "c3pool.com"
                url = f"https://api.{domain}/miner/{self.wallet}/stats"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    unpaid = data.get("amtDue", 0) / 1000000000000
                    total_paid = data.get("amtPaid", 0) / 1000000000000

            elif "herominers.com" in self.pool:
                url = f"https://monero.herominers.com/api/stats_address?address={self.wallet}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    stats = data.get("stats", {})
                    unpaid = stats.get("balance", 0) / 1000000000000
                    total_paid = stats.get("paid", 0) / 1000000000000

            elif "supportxmr.com" in self.pool:
                url = f"https://supportxmr.com/api/miner/{self.wallet}/stats"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    unpaid = data.get("amtDue", 0) / 1000000000000
                    total_paid = data.get("amtPaid", 0) / 1000000000000

            elif "nanopool.org" in self.pool:
                url = f"https://xmr.nanopool.org/api/v1/user/{self.wallet}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json().get("data", {})
                    unpaid = float(data.get("balance", 0))
            self.stats_updated.emit({"unpaid": unpaid, "paid": total_paid})
            
        except Exception as e:
            print(f"[DEBUG] Pool API fetch failed: {e}")