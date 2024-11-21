from raydium import buy, sell
from utils import get_pair_address, fetch_pool_keys, get_token_price, get_token_balance
import time

class RaydiumTrade:
    def __init__(self, token_address:str, sol_in:float=0.1, target_percent:int=100, stop_loss_percent:int=10, slippage:int=5, percentage:int=100, refresh:int=3):
        self.token_address = token_address
        self.sol_in = sol_in
        self.slippage = slippage
        self.percentage = percentage
        self.target_percent = target_percent
        self.stop_loss_percent = stop_loss_percent
        self.pair_address = get_pair_address(self.token_address)
        self.pool_keys = None
        self.token_balance = None
        self.initial_value = None
        self.target_value = None
        self.stop_loss_value = None
        self.refresh = 3

    def start(self):
        print("🤖 Starting the Raydium trading bot...")
        
        if self.pair_address:
            if self.buy_token():
                self.fetch_pool_keys()
                if self.get_token_balance():
                    self.calculate_initial_value()
                    self.calculate_targets()
                    self.monitor_market()
                else:
                    print(f"❌ Failed to fetch token balance after multiple attempts...")
            else:
                print("❌ Buy operation failed.")
        else:
            print("❌ Pair address not found...")

    def buy_token(self):
        if buy(self.pair_address, self.sol_in, self.slippage):
            print("✅ Buy executed successfully.")
            return True
        return False

    def fetch_pool_keys(self):
        self.pool_keys = fetch_pool_keys(self.pair_address)

    def get_token_balance(self, attempts=10):
        print("Attempting to fetch token balance... ")
        time.sleep(5)
        for attempt in range(attempts):
            self.token_balance = get_token_balance(self.token_address)
            if self.token_balance:
                print(f"Token Balance: {self.token_balance}")
                return True
            else:
                print(f"Attempt {attempt + 1} to fetch token balance failed.")
                time.sleep(5)
        return False

    def calculate_initial_value(self):
        initial_token_price, _ = get_token_price(self.pool_keys)
        self.initial_value = self.token_balance * initial_token_price
        print(f"Initial Value: {self.initial_value}")

    def calculate_targets(self):
        self.target_value = (1 + (self.target_percent / 100)) * self.initial_value
        self.stop_loss_value = (1 - (self.stop_loss_percent / 100)) * self.initial_value

    def monitor_market(self):
        while True:
            try:
                token_price, _ = get_token_price(self.pool_keys)
                current_value = self.token_balance * token_price
                print(f"Current Value: {current_value} -> 🎯 Target: {self.target_value} | 🛑 Stop-Loss: {self.stop_loss_value}", end='\r')

                if current_value >= self.target_value:
                    print("\n💥 Target hit! Executing sell...")
                    if self.sell_token():
                        break

                elif current_value <= self.stop_loss_value:
                    print("\n🛑 Stop-loss triggered! Executing sell...")
                    if self.sell_token():
                        break

                time.sleep(self.refresh)
            except Exception as e:
                print(f"\n⚠️ An error occurred: {e}")

    def sell_token(self):
        if sell(self.pair_address, self.percentage, self.slippage):
            print("✅ Sell executed successfully.")
            return True
        return False
