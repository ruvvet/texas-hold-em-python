from cards import Cards

# Community Class
# Manages community cards on the table
# Manages most shared states/variables
class Community:

    def __init__(self, deck, blind):
        self.comm_cards = []
        self.deck = deck
        self.pot = 0
        self.match_raise = 0
        self.cards = Cards(self.comm_cards)
        self.blind_amt = blind

    # Draws n cards based on the draw round it is in
    def community_hand(self, n):
        if n != 0:
            print('... Dealing {n} cards...'.format(n=n))
        for card in self.deck.draw(n):
            self.comm_cards.append(card)

    # Updates pot as bets are made
    def update_pot(self, bet_amt):
        # Update raise amt if higher than current
        # if bet_amt > self.match_raise:
        #     self.match_raise = bet_amt

        # Update pot
        self.pot += bet_amt
        
    # Update check state to false if a bet was made
    # If no raises were made, ie: match_raise = 0
    # Players can check
    def can_check(self):
        # list true if no player raised
        # filter filters out any false values from the list (none, list)
        # if the len of the filter is not equal to len of players
        # someone called raise
        # therefore false
        # if player_call == 'R':
        #     self.check = False
        # else:
        #     self.check = True
        #return len(list(filter(None,[True if player.player_call != 'R' else False for player_num, player in self.players.items()]))) == len(self.players.keys())
        return self.match_raise ==0
