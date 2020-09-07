import random


# Dealer Class
# Hanldes who is the dealer, big/little blind
# Takes players, blind amt, community as arguments
class Dealer:

    def __init__(self, players, blind, community):
        self.players = players
        self.blind_amt = blind
        self.community = community
   
        # This randomly selects a random player to start as the first dealer
        self.dealer = random.randint(0,len(players)-1)

    # If the player number = the dealer #, that player is the dealer
    # Sets the is_dealer variable in the player class to true
    # Uses modulo to set the other blinds
    # might need to do -1, -2 as blinds should be to the left of the dealer
    def set_blinds(self):
        print('dealer', self.dealer+1)
        for player_num, player in self.players.items():
            if player_num == self.dealer + 1:
                player.is_dealer = True
            if player_num == ((self.dealer + 1) % len(self.players)) + 1:
                player.is_big_blind = True
                player.bet_amt = self.blind_amt*2
            if player_num == ((self.dealer + 2) % len(self.players)) + 1:
                player.is_little_blind = True
                player.bet_amt = self.blind_amt
         

    def bet_order(self):
        self.betting_order = [(((self.dealer + x) % len(self.players)) + 1) for x in self.players.keys()]
        self.order = {order:self.players[order] for order in self.betting_order}
        print(self.betting_order)
        print(self.order)
        
        return self.order