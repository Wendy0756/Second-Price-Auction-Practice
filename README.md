# Online Second-Price Auction System

This project implements an online second-price auction system for ad placement, where bidders compete to show ads to users. The system uses a second-price sealed-bid auction mechanism (also known as a Vickrey auction), where the highest bidder wins but pays the second-highest bid price.

## Overview

The auction system consists of three main components:
- **User**: Represents a user with a probability of clicking on ads
- **Bidder**: An intelligent bidding agent that learns from historical user performance
- **Auction**: Manages the auction rounds and determines winners

## Classes

### User (`auction_Tian.py`)

The `User` class represents a user in the system with an inherent probability of clicking on ads.

**Attributes:**
- `_User__probability`: A randomly generated probability (0-1) that determines the user's likelihood of clicking on an ad

**Methods:**
- `show_ad()`: Simulates showing an ad to the user. Returns `True` if the user clicks, `False` otherwise. The result is based on the user's probability.

**Example:**
```python
user = User()
clicked = user.show_ad()  # Returns True or False based on user's probability
```

### Bidder (`bidder_Tian.py`)

The `Bidder` class represents an intelligent bidding agent that learns from historical data to optimize bidding strategies.

**Initialization:**
- `num_users`: Total number of users in the system
- `num_rounds`: Total number of auction rounds

**Attributes:**
- `dict`: Dictionary storing user performance data in format `{user_id: [total_outcome, occurrence_count]}`
- `round`: Remaining number of rounds
- `balance`: Current balance (profit/loss)
- `user_id`: ID of the user in the current round

**Methods:**
- `bid(user_id)`: Returns a bid amount for the given user based on historical performance
  - If user has sufficient historical data and performed well (score > 0.5), bids the score
  - If user has sufficient data but performed poorly, bids randomly between 0 and score
  - If user has insufficient data or is new, bids randomly between 0 and 0.5
  - Returns 0 if no rounds remain
  
- `notify(auction_winner, price, clicked)`: Updates bidder's state after auction results
  - If winner: Updates user performance data and balance
  - Returns a message with auction results

**Bidding Strategy:**
The bidder uses an adaptive learning strategy:
1. **Sufficient data condition**: User has been seen more than 1% of remaining rounds OR bidder has seen 50% of all users
2. **High performer (score > 0.5)**: Bid the exact score
3. **Low performer (score ≤ 0.5)**: Bid conservatively (random between 0 and score)
4. **Insufficient data**: Bid conservatively (random between 0 and 0.5)

### Auction (`auction_Tian.py`)

The `Auction` class manages the auction process and executes rounds.

**Initialization:**
- `users`: List of User objects
- `bidders`: List of Bidder objects

**Attributes:**
- `bidders`: List of participating bidders
- `users`: List of users in the system
- `balances`: Dictionary tracking each bidder's balance
- `winner`: The winning bidder in the current round
- `price`: The price paid by the winner (second-highest bid)

**Methods:**
- `execute_round()`: Executes a single auction round
  1. Randomly selects a user
  2. Collects bids from all qualified bidders (balance >= -1000)
  3. Determines winner using second-price auction rules
  4. Shows ad to selected user
  5. Updates winner's balance: `balance = balance - price + clicked` (where clicked is 1 if ad was clicked, 0 otherwise)
  6. Notifies all bidders of the results

**Auction Rules:**
- **Second-Price Auction**: Winner pays the second-highest bid
- **Tie Handling**: If multiple bidders have the same highest bid, winner is chosen randomly and pays that bid amount
- **Qualification**: Bidders with balance < -1000 are disqualified
- **Exception**: Auction ends if no qualified bidders remain

## Requirements

- Python 3.x
- NumPy

Install NumPy:
```bash
pip install numpy
```

## Usage Example

```python
import numpy as np
from auction_Tian import User, Auction
from bidder_Tian import Bidder

# Create users
num_users = 100
users = [User() for _ in range(num_users)]

# Create bidders
num_rounds = 1000
bidders = [Bidder(num_users, num_rounds) for _ in range(5)]

# Create auction
auction = Auction(users, bidders)

# Run auction rounds
for round_num in range(num_rounds):
    try:
        auction.execute_round()
        print(f"Round {round_num + 1}: Winner balance = {auction.balances[auction.winner]}")
    except Exception as e:
        print(f"Auction ended: {e}")
        break

# Check final balances
for bidder in bidders:
    print(f"Bidder final balance: {bidder.balance}")
```

## How It Works

1. **Initialization**: Create users with random click probabilities and bidders with learning capabilities
2. **Auction Round**:
   - A random user is selected
   - Each qualified bidder submits a bid based on their learning strategy
   - The highest bidder wins
   - Winner pays the second-highest bid
   - Ad is shown to the user
   - Winner's balance is updated: `balance = balance - price + (1 if clicked else 0)`
   - All bidders are notified and update their learning data
3. **Learning**: Bidders track user performance and adjust bids accordingly
4. **Termination**: Auction ends when no qualified bidders remain or rounds are exhausted

## Notes

- User click probabilities are randomly generated and remain constant throughout the auction
- Bidders learn from historical performance to optimize their bidding strategy
- The second-price auction mechanism encourages truthful bidding
- Bidders are disqualified if their balance falls below -1000

