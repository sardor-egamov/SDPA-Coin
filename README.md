SDPA Coin Market Simulation
https://github.com/sardor2412/oi23453_EMATM004

Overview
This project simulates a cryptocurrency market environment, focusing on user interactions within a digital currency market named SDPA Coin. The simulation is implemented in Python and is structured into two main files: SDPA_Coin.py and main.py.

SDPA_Coin.py
This file contains the essential classes that define the simulation's mechanics:

UserAccount: Represents an individual's account in the SDPA Coin market. It includes attributes like the user's balance in GBP, SDPA Coin balance, and mining machines. Functions in this class allow users to buy/sell SDPA Coin, manage mining machines, and deal with expenses like electricity costs.

BlockchainSystem: Functions as the record-keeping system, tracking all transactions within the market. It maintains a ledger of SDPA Coin distributions and mined amounts.

Market: Models the market dynamics. It maintains the market's liquidity, manages the supply of SDPA Coin and mining machines, and regulates prices based on market activities.

main.py
This script serves as the main interface for running the simulation. It orchestrates the market simulation over a user-defined number of days. Key features include:

User Interactions: Allows simulated users to interact with the market by buying or selling SDPA Coin, trading mining machines, and more.

Daily Market Updates: The script processes daily market changes, updates prices, and distributes SDPA Coin.

Visualization: Utilizes Matplotlib to graphically represent the progression of SDPA Coin prices and the asset values of users over time.

Design Considerations
The project adheres to object-oriented principles, ensuring clarity and modularity. Distinct responsibilities are assigned to each class, aligning with the single-responsibility principle. This design facilitates easier maintenance and potential future expansions of the project.

Conclusion
The SDPA Coin Market Simulation offers an insightful look into cryptocurrency market operations. It serves as an educational tool for understanding the dynamics of digital currency trading and blockchain technology.
