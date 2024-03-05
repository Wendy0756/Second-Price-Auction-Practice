import numpy as np
class User:
    '''
    Create a "User" class with an attribute: probability of clicking on the ads.
    '''
    def __init__(self):
        self._User__probability = np.random.uniform()
       
    def __repr__(self):
        return f'{User} with secret likelihood of clicking on an ads: {self._User__probability}.'
    
    def __str__(self):
        return str(User)+ " with secret likelihood of clicking on an ads: " + str(self._User__probability)
    
    def show_ad(self):
        # return True if the user click on the ads
        result = np.random.choice([True, False], p = [self._User__probability, 1-self._User__probability]) 
        return result

class Auction:
    '''Class to represent an online second-price auction'''
    
    def __init__(self, users, bidders):
        '''Initializing users, bidders, and dictionary to store balances for each bidder in the auction'''
        self.bidders = bidders
        self.users = users
        # Create dictionary to store bidder's balance at the beginning of each round.
        self.balances = {}
        self.winner = ''
        for bidder in bidders:
            self.balances[bidder] = 0
        
    def execute_round(self):
        # Create list to store bidder's bid amount in each round
        self.bid_list = []
        # This method executes all steps witin a single round of auction.
        
        # Randomly select a user and show user_id for bidding
        c = np.random.randint(0, len(self.users))
        
        # Each bidders bid.
        # Create bid_list to store all bidders' bid amounts in current round.
        qualified_bidder = 0
        for bidder in self.bidders: 
            self.bid_list.append(bidder.bid(c))
            # Bid from qualified bidders only - replace the unqualified user's bid with (-1).
            if self.balances[bidder] >= -1000:
                qualified_bidder += 1
            else:
                self.bid_list[self.bidders.index(bidder)] = -1
       
        # Selection of winning bidders and actual price based on the bid_list.
        if qualified_bidder == 0:
            raise Exception('There is no qualified bidder. Auction ends!')
        elif qualified_bidder == 1:
            self.winner = self.bidders[self.bid_list.index(max(self.bid_list))]
            self.price = max(self.bid_list)
        else:
            max_bid = max(self.bid_list)
            # Condition #1: more than 1 bidder gave the same highest bid:
            if self.bid_list.count(max_bid) > 1:
                self.price = max_bid
                # Create w_list to store the top bidders' indexes
                w_list = []
                for i in range(len(self.bid_list)):
                    if self.bid_list[i] == max_bid:
                        w_list.append(i)
                # Calculate the probability that each of the winners get chosen 
                prob_win = 1/len(w_list)
                w = np.random.choice(w_list, p = [prob_win] * len(w_list))
                self.winner = self.bidders[w]
            # Condition #2: Only 1 bidder gave the highest bid:
            else:
                self.bid_list2 = [x for x in self.bid_list if x != max_bid]
                self.price = max(self.bid_list2)
                w = self.bid_list.index(max_bid)
                #print(len(self.bidders), w, self.bid_list)
                self.winner = self.bidders[w]
            
        # Show an ad to the chosen user and find out if clicked:
        clicked = self.users[c].show_ad()

        # Update the class attribute internally
        self.balances[self.winner] = self.balances[self.winner] - self.price + clicked

        # Notifying each bidders the bidding result
        for x in self.bidders:
            if x == self.winner:
                x.notify(True, self.price, clicked)
            else:
                x.notify(False, self.price, None)