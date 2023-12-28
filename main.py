
from SDPA_Coin import UserAccount, Market, BlockchainSystem

# Initialization
market = Market()
blockchain = BlockchainSystem()
users = []
usernames = set()  # To track unique usernames

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
            
for day in range(1, days_to_simulate + 1):
    print(f"\n================================\n====== Simulation Day {day} ======\n================================")

    # Display the current day's prices (set on the previous day, or initial values for Day 1)
    print(f"The price of SDPA is {market.sdpa_price: }. Electricity unit cost {market.electricity_price:.4f}. Total number of mining machines {market.mining_machines}.")

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
            action = get_integer_input("Choose an action - 1: Buy SDPA, 2: Sell SDPA, 3: Buy Mining Machine, 4: End Turn: ", 1)
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
                user.deduct_electricity_cost(market)
                break
            
        initial_investment=10000
        balance = user.gbp_capital
        sdpa_value = user.sdpa_balance * market.sdpa_price  # Calculate with the final market price
        mining_machine_investment = user.mining_machines * market.mining_machine_cost
        profit_loss = balance + sdpa_value - initial_investment - mining_machine_investment

        print(f"\nUser: {user.username}")
        print(f"Value of SDPA Holdings: {sdpa_value:.4f} GBP")
        print(f"Profit/Loss: {profit_loss:.4f} GBP\n")

        # Check for bankruptcy
        user.check_and_declare_bankruptcy(market)
        
    # Generate the prices for the next day at the end of the current day
    market.deduct_market_electricity_cost()
    market.generate_daily_prices()
    

print("\nSimulation completed. Final state:")

for user in users:
    print(f"User: {user.username}")
    print("Initial Investment: 10000 GBP")
    print(f"Balance: {balance:.4f} GBP")
    print(f"Value of SDPA Holdings: {sdpa_value:.4f} GBP")
    print(f"Investment in Mining Machines: {mining_machine_investment:.4f} GBP")
    print(f"Profit/Loss: {profit_loss:.4f} GBP\n")
    

    
    

