import random
import numpy as np


class UserAccount:
    def __init__(self, username, initial_capital=10000):
        self.username = username
        self.capital = initial_capital
        self.sdpa_balance = 0
        self.mining_machines = 0

    def buy_sdpa(self, amount, market):
        
        total_cost = amount * market.sdpa_price
        if self.capital >= total_cost:
            self.sdpa_balance += amount
            self.capital -= total_cost
            return f"{amount} SDPA purchased for {total_cost} GBP."
        else:
            return "Insufficient capital to buy SDPA."
        

    def sell_sdpa(self, amount, market):
        if self.sdpa_balance >= amount:
            revenue = amount * market.sdpa_price
            self.sdpa_balance -= amount
            self.capital += revenue
            return f"{amount} SDPA sold for {revenue} GBP."
        else:
            return "Insufficient SDPA to sell."
        

    def buy_mining_machine(self, market):
        



class BlockchainSystem:
    def __init__(self):
        self.transactions = []  
        self.total_sdpa_mined = 0  
        self.daily_sdpa_generation = 100  

    def distribute_sdpa(self, users):
        


class Market:
    def __init__(self):
        self.gbp_balance = 100000000  
        self.sdpa_balance = 100000000  
        self.mining_machines = 1000  
        self.sdpa_price = 40  
        self.electricity_price = random.uniform(1.9, 2.1) 
        self.mining_machine_cost = 600 

    def generate_daily_prices(self):
       