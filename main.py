from SDPA_Coin import UserAccount, Market, BlockchainSystem
import matplotlib.pyplot as plt

# Initialization
market = Market()
blockchain = BlockchainSystem()
users = []
usernames = set()  # To track unique usernames
sdpa_price_list = []

def get_integer_input(prompt, min_value=None):
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Value should be at least {min_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")
            
def get_float_input(prompt, min_value=None):
    while True:
        try:
            value = float(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Value should be at least {min_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")
    
            
# Get simulation parameters from user
days_to_simulate = get_integer_input(">>> Please enter the number of Days to simulate: ", 1)
num_users = get_integer_input(">>> Please enter the number of Users: ", 1)

# Create user accounts
for i in range(1, num_users + 1):
    while True:
        name = input(f">>> Please enter the name of User{i}: ")
        if name not in usernames:
            users.append(UserAccount(name, 10000, 0, 0))  # Starting with 10000 GBP, 0 SDPA, 0 machines
            usernames.add(name)  # Add to the set of usernames
            break
        else:
            print("Username already taken. Please choose a different username.")

# Initialize asset tracking for each useк
user_asset_values = {user.username: [] for user in users}
            
for day in range(1, days_to_simulate + 1):
    print(f"\n================================\n====== Simulation Day {day} ======\n================================")

    # Display the current day's prices (set on the previous day, or initial values for Day 1)
    print(f"The price of SDPA is {market.sdpa_price: }. The price of Mining Machine is is {market.mining_machine_cost: }, the sale price of Mining Machine is {market.mining_machine_price_to_sell}. Electricity unit cost {market.electricity_price:.4f}. The total number of mining machines {market.mining_machines}.")

    # Distribute SDPA to miners
    blockchain.distribute_sdpa(users, market)
    # Create a copy of the users list to iterate over
    active_users = users.copy()

    # Daily user interactions
    for user in users:
        # Skip users who have been declared bankrupt
        if user.gbp_capital <= 0:
            continue
        print(f"\nUser: {user.username}, Balance: {user.gbp_capital: .4f} GBP, SDPA: {user.sdpa_balance}, Mining Machines: {user.mining_machines}")
        sdpa_value = user.sdpa_balance * market.sdpa_price
        print(f"User: {user.username}, SDPA Holdings Value: {sdpa_value:} GBP, price: {market.sdpa_price}")
        while True:
            action = get_integer_input("Choose an action - 1: Buy SDPA, 2: Sell SDPA, 3: Buy Mining Machine, 4: Sell Mining Machine, 5: Toggle Mining Machine, 6: End Turn: ", 1)
            if action == 1:
                amount = get_float_input("Enter amount of SDPA to buy: ", 0.01)
                user.buy_sdpa(amount, market)
            elif action == 2:
                amount = get_float_input("Enter amount of SDPA to sell: ", 0.01)
                user.sell_sdpa(amount, market)
            elif action == 3:
                amount = get_integer_input("Enter number of mining machines to buy: ", 1)
                user.buy_mining_machine(amount, market)
            elif action == 4:
                amount = get_integer_input("Enter number of mining machines to sell: ", 1)
                user.sell_mining_machine(amount, market)
            elif action == 5:
                user.toggle_mining_machines()
            elif action == 6:
                user.deduct_electricity_cost(market)
                break
        # Check for bankruptcy
        user.check_and_declare_bankruptcy(market)
        
    # Update SDPA price and asset values at the end of the day  and display financial info
    sdpa_price_list.append(market.sdpa_price)
    for user in users:
        asset_value = user.gbp_capital + (user.sdpa_balance * market.sdpa_price) + (user.mining_machines * market.mining_machine_price_to_sell)
        user_asset_values[user.username].append(asset_value)
        initial_investment=10000
        balance = user.gbp_capital
        sdpa_value = user.sdpa_balance * market.sdpa_price  # Calculate with the final market price
        mining_machine_value = user.mining_machines * market.mining_machine_price_to_sell
        profit_loss = balance + sdpa_value + mining_machine_value - initial_investment 

        print(f"\nUser: {user.username}")
        print(f"Balance: {balance:.4f} GBP")
        print(f"Value of SDPA Holdings: {sdpa_value:.4f} GBP")
        print(f"Value of Mining Machines Holdings: {mining_machine_value:.4f} GBP")
        print(f"Profit/Loss: {profit_loss:.4f} GBP\n")
        
        
    # Generate the prices for the next day at the end of the current day
    market.deduct_market_electricity_cost()
    market.generate_daily_prices()
    

print("\nSimulation completed. Final state:")

for user in users:
    balance = user.gbp_capital
    sdpa_value = user.sdpa_balance * market.sdpa_price
    mining_machine_value = user.mining_machines * market.mining_machine_price_to_sell
    profit_loss = balance + sdpa_value + mining_machine_value - initial_investment
    print(f"\nUser: {user.username}")
    print("Initial Investment: 10000 GBP")
    print(f"Balance: {balance:.4f} GBP")
    print(f"Value of SDPA Holdings: {sdpa_value:.4f} GBP")
    print(f"Value of Mining Machines Holdings: {mining_machine_value:.4f} GBP")
    print(f"Profit/Loss: {profit_loss:.4f} GBP\n")


transactions = market.get_transaction_records()
for transaction in transactions:
    print(transaction)

days = list(range(1, days_to_simulate + 1))
# Visualization after Simulation
plt.figure(figsize=(12, 6))
plt.plot(days, sdpa_price_list, label='SDPA Price')
plt.title('SDPA Price Over Time')
plt.xlabel('Day')
plt.xticks(range(1, days_to_simulate + 1))
plt.ylabel('Price')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
for username, asset_values in user_asset_values.items():
    plt.plot(days, asset_values, label=f"{username}'s Asset Value")
plt.title('User Asset Values Over Time')
plt.xlabel('Day')
plt.xticks(range(1, days_to_simulate + 1))
plt.ylabel('Asset Value')
plt.legend()
plt.show()
    

    

    
    

