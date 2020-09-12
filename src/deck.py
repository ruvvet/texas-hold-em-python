import random


# Deck Class
#   Manages the deck of cards
#   Is called whenever a card/s is drawn
#   Keeps track of deck "order",
#   which cards are in play, and which cards remain
#   Deals from top/beginning of the list to players/table
class Deck:

    def __init__(self):
        self.deck_val = '23456789TJQKA'
        self.deck_suit = 'CDHS'
        # Make the full 52 card deck
        self.full_deck = [
            ''.join([val, suit])
            for suit in self.deck_suit
            for val in self.deck_val
            ]
        # Shuffle the deck
        self.shuffle_deck()

    # Shuffles the deck
    def shuffle_deck(self):
        random.shuffle(self.full_deck)
        return self.full_deck

    # Draws n cards
    def draw(self, n):
        cards = []
        for i in range(n):
            cards.append(self.full_deck.pop(0))
        return cards
