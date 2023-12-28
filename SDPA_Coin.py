import random
import numpy as np

class UserAccount:
    def __init__(self, username, gbp_capital, sdpa_balance, mining_machines):
        """
        Initializes a new user account with the specified username, GBP capital, SDPA balance, and number of mining machines.
        """
        self.username = username
        self.gbp_capital = gbp_capital
        self.sdpa_balance = sdpa_balance
        self.mining_machines = mining_machines

    def buy_sdpa(self, amount, market):
        """
        Allows the user to buy a specified amount of SDPA at the current market price.
        The user's GBP capital is updated accordingly.
        """
        cost = market.get_sdpa_price() * amount
        if cost <= self.gbp_capital:
            market.execute_trade(self, amount, "buy")
            print(f"{self.username} bought {amount} SDPA. New balance: {self.gbp_capital:.2f} GBP")
        else:
            print("Not enough GBP capital to complete this purchase.")
        
    def sell_sdpa(self, amount, market):
        """
        Allows the user to sell a specified amount of SDPA at the current market price.
        The user's GBP capital is updated accordingly.
        """
        if amount <= self.sdpa_balance:
            market.execute_trade(self, amount, "sell")
            print(f"{self.username} sold {amount} SDPA. New balance: {self.gbp_capital:.2f} GBP")
        else:
            print("Not enough SDPA balance to complete this sale.")
        
    def buy_mining_machine(self, quantity, market):
        """
        Allows the user to purchase a specified number of mining machines at the market's current price.
        The user's GBP capital and number of mining machines are updated accordingly.
        """
        total_cost = market.mining_machine_cost * quantity
        if total_cost <= self.gbp_capital:
            market.execute_buy_mining_machines(self,quantity)
            print(f"{self.username} bought {quantity} mining machines. New balance: {self.gbp_capital:.2f} GBP")
        else:
            print("Not enough GBP capital to buy mining machines.")
            
    def deduct_electricity_cost(self, market):
        total_cost = market.electricity_price * self.mining_machines
        if self.gbp_capital >= total_cost:
            market.execute_deduct_electricity_cost(self, total_cost)
        else:
            # Handle the scenario when the user cannot pay for the electricity
            print("Insufficient funds to cover electricity costs.")
            
    def check_and_declare_bankruptcy(self, market):
                    
        """
        Checks if the user is bankrupt and initiates the bankruptcy process if necessary.
        """
        if self.gbp_capital <= 0:
            market.execute_bankruptcy(self)


class BlockchainSystem:
    def __init__(self):
        """
        Initializes the blockchain system, setting up a list to store transactions and counters for mined SDPA.
        """
        self.transactions = []  # List to store all transactions
        self.total_sdpa_mined = 0  # Total SDPA mined in the system
        self.daily_sdpa_generation = 100  # Total SDPA generated daily

    def distribute_sdpa(self, user_accounts, market):
        """
        Distributes the daily SDPA generation among users and market.
        Updates each user's and market's SDPA balance and records the transaction.
        """
        total_mining_machines = sum(user.mining_machines for user in user_accounts) + market.mining_machines
        if total_mining_machines == 0:
            return  # No mining machines in the system, no distribution

        for user in user_accounts:
            if user.mining_machines > 0:
                generated_sdpa = (user.mining_machines / total_mining_machines) * self.daily_sdpa_generation
                user.sdpa_balance += generated_sdpa
                self.total_sdpa_mined += generated_sdpa
                self.record_transaction({
                    'type': 'mining_reward',
                    'user': user.username,
                    'amount': generated_sdpa
                })

    def record_transaction(self, transaction):
        """
        Records a transaction in the blockchain system.
        """
        self.transactions.append(transaction)

class Market:
    def __init__(self):
        """
        Initializes the market with a large balance of GBP and SDPA, a set of mining machines, and initial prices for SDPA and electricity.
        """
        self.gbp_balance = 100000000  # Huge initial GBP balance to simulate infinite capital
        self.sdpa_balance = 100000000  # Huge initial SDPA balance
        self.mining_machines = 1000  # 1000 mining mining machines
        self.sdpa_price = 40  # Initial SDPA price
        self.electricity_price = random.uniform(1.9, 2.1)  # Initial electricity price
        self.mining_machine_cost = 600 # Cost of a mining machine

    def generate_daily_prices(self):
        """
        Generates daily prices for SDPA and electricity based on specified distributions.
        """
        daily_return = np.random.normal(0.003, 0.0016)
        new_price = self.sdpa_price * (1 + daily_return)
        self.sdpa_price = new_price
        self.electricity_price = random.uniform(1.9, 2.1)

    def execute_trade(self, user, amount, trade_type):
        """
        Executes a trade where the user can buy or sell SDPA.
        Updates the market and user balances based on the trade.
        """
        if trade_type == "buy" and amount * self.sdpa_price <= user.gbp_capital:
            self.gbp_balance += amount * self.sdpa_price
            user.gbp_capital -= amount * self.sdpa_price
            self.sdpa_balance -= amount
            user.sdpa_balance += amount
        elif trade_type == "sell" and amount <= user.sdpa_balance:
            self.gbp_balance -= amount * self.sdpa_price
            user.gbp_capital += amount * self.sdpa_price
            self.sdpa_balance += amount
            user.sdpa_balance -= amount
        else:
            #UserAccount class already covers the following scenario. Added as an additional safety net.
            print("Trade cannot be executed due to insufficient funds or balance.")
            
    def execute_buy_mining_machines(self, user, quantity):
        """
        Handles the purchase of mining machines by a user.
        """
        total_cost = self.mining_machine_cost * quantity
        if user.gbp_capital >= total_cost and self.mining_machines >= quantity:
            user.gbp_capital -= total_cost
            user.mining_machines += quantity
            self.mining_machines -= quantity  # Update the number of mining machines in the market
            print(f"{user.username} purchased {quantity} mining machines.")
        #UserAccount class already covers the following scenario. Added as an additional safety net.
        else:
            print(f"{user.username} cannot afford to buy {quantity} mining machines or not enough machines in the market.") 

    def execute_deduct_electricity_cost(self, user, total_cost):
        if user.gbp_capital >= total_cost:
            user.gbp_capital -= total_cost
            print(f"Electricity cost of {total_cost:.2f} GBP deducted from {user.username}'s account.")
        else:
            print(f"{user.username} does not have enough funds to cover electricity costs.")

    def get_sdpa_price(self):
        """
        Returns the current price of SDPA.
        """
        return self.sdpa_price
        
    def deduct_market_electricity_cost(self):
        total_cost = self.electricity_price * self.mining_machines
        self.gbp_balance -= total_cost
        print(f"Market paid {total_cost:.4f} GBP for electricity. New balance: {self.gbp_balance:.4f} GBP")
