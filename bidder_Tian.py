import math
import numpy as np
class Bidder:
    def __init__(self, num_users, num_rounds):
        # Create dictionary {user_id: (total outcome, # of occurance)} to store user's average outcome if applicable.
        self.dict = {-1:[0,0]}
        self.round = num_rounds
        self.num_users = num_users
        self.balance = 0
    
    def __repr__(self):
        return f'{Bidder} object with balance: {self.balance}'
    
    def __str__(self):
        return f'{Bidder} object with balance: {self.balance}'
    
    def bid(self, user_id):
        # This method takes in the user_id and returns the bid on that user, rounds to 3 decimal places.
        self.user_id = user_id
        if self.round > 0:
            self.round -= 1
            # If the user_id is in our dictionary, calculate the user's average performance score.
            if user_id in self.dict:
                score = self.dict[user_id][0]/self.dict[user_id][1]
                '''
                The strategy is: 
                >> If the user has enough record - Having gone through 1% of the rounds left or having saw 50% of the users'results: 
                (1) if the users performed well (score > 0.5), we will bid the score.
                (2) if the user didn't perform well (score < 0.5), we will randomly bid (0, score) to be conservative.
                >> If the user's record is not enough, we will be conservative: randomly bid (0, 0.5).
                >> If the user never showed up before, we will bid randomly (0, 0.5).
                '''
                if self.dict[user_id][1] > int(math.ceil(0.01 * self.round)) or len(self.dict) >= 0.05 * self.num_users:
                    if score > 0.5:
                        bidding = round(score,3)
                    else:
                        bidding = round(np.random.uniform(0, score),3)
                else:
                    bidding = round(np.random.uniform(0, 0.5),3)
            else:
                bidding = round(np.random.uniform(0, 0.5),3)
            return bidding    
        else:
            return 0
    
    def notify(self, auction_winner, price, clicked):
        if auction_winner:
            # Store the user's performance in the dictionary:
            if self.user_id in self.dict:
                self.dict[self.user_id][0] += clicked
                self.dict[self.user_id][1] += 1
            else:
                self.dict[self.user_id] = [0, 0]
                self.dict[self.user_id][0] = clicked
                self.dict[self.user_id][1] = 1
            self.balance = self.balance + clicked - price
            return f'Congrats! You won. The winning price is {price}. User# {self.user_id} outcome is {clicked}. Your current balance is {self.balance}.'
        else:
            return f'Sorry. You lost. The winning price is {price}.'
            