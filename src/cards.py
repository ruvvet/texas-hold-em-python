# Cards Class
#   Defines the value of the cards in the deck and return a formatted version
#   Calculates the value of the hand
#   Prettifies the card
class Cards:

    def __init__(self, hand):
        self.CARD_V = '23456789TJQKA'
        # Create a dictionary where key = card value, value = index position + 2
        # Yields the same result as a full listed out dictionary
        self.CARD_VALUES = dict(zip(list(self.CARD_V), range(2, 15)))
        self.REVERSE_CARD_VALUES = {v:k for (k,v) in self.CARD_VALUES.items()}
        self.CARD_SUITS = {
            'C': '♣',
            'D': '♢',
            'H': '♡',
            'S': '♠'
        }
        self.HAND_TYPES = ['High Card', 'Pair', 'Two Pair', 'Three of a Kind',
        'Straight', 'Flush', 'Full House', 'Four of a Kind', 'Straight Flush',
        'Royal Flush']
        self.RANKED_HAND_TYPES = dict(zip([x for x in range(10)], self.HAND_TYPES))
        
        #self.evaluate_hand = self.evaluate_hand()

    # Takes the players cards +  community cards to create the full hand
    # Calls the evaluate_hand function
    def get_hand(self, player_cards, community_cards):
        self.hand = player_cards + community_cards
        # Gives all the values in the hand
        self.values = [i[0] for i in self.hand if i[0] in self.CARD_VALUES.keys()]
        # Gives all the suits in the hand
        self.suits = [j[1] for j in self.hand if j[1] in self.CARD_SUITS.keys()]
        # Sorts all values in hand in desc order
        self.sort_hand = sorted([self.CARD_VALUES[i] for i in self.values], reverse=True)
        # Gives dictionary of count of cards in hand
        self.COUNT = {k:self.values.count(k) for k in self.CARD_V}
        if len(self.hand) <5:
            return self.high_card()[1]
        else:
            return self.evaluate_hand()

    # Returns top hand, top card from top hand, + kickers as a list
    def evaluate_hand(self):
        # List of the functions of hand types
        self.HANDS = [self.high_card(),self.pair(), self.two_pair(),self.three_kind(),self.straight(), self.flush(), self.full_house(), self.four_kind(), self.straight_flush(), self.royal_flush()]
        # Dictionary of the functions of hand types
        self.RANKED_HANDS = dict(zip([x for x in range(10)], self.HANDS))
        self.best_hand = sorted([k for k,v in self.RANKED_HANDS.items() if v[0] == True], reverse = True)[0]
        self.top_card = [v[1] for k,v in self.RANKED_HANDS.items() if k == self.best_hand]
        self.kickers = [x for x in self.sort_hand if x != self.top_card[0]]
        self.card_eval = []
        self.card_eval.append(self.best_hand)
        self.card_eval = self.card_eval + self.top_card + self.kickers
        return self.card_eval

    def high_card(self):
        return True, self.sort_hand[0]

    def pair(self):
        if 2 in self.COUNT.values():
            pair = sorted([self.CARD_VALUES[k] for k, v in self.COUNT.items() if v == 2], reverse= True)
            return len(pair) == 1, pair[0]
        return False, 0

    def two_pair(self):
        if 2 in self.COUNT.values():
            pairs = sorted([self.CARD_VALUES[k] for k, v in self.COUNT.items() if v == 2], reverse= True)
            return len(pairs)==2, pairs[0]
        return False, 0

    def three_kind(self):
        if 3 in self.COUNT.values():
            three = sorted([self.CARD_VALUES[k] for k, v in self.COUNT.items() if v == 3], reverse = True)
            return len(three) == 1, three[0]
        return False, 0

    def straight(self):
        return ''.join(map(str, self.sort_hand)) in '14131211109876543214', self.sort_hand[0]

    def flush(self):
        return len(set(self.suits)) == 1, self.sort_hand[0]

    def full_house(self):
        return self.pair()[0] and self.three_kind()[0], self.three_kind()[1]

    def four_kind(self):
        if 4 in self.COUNT.values():
            four = sorted([self.CARD_VALUES[key] for k, v in self.COUNT.items() if v == 4], reverse = True)
            return len(four)==1, four[0]
        return False, 0

    def straight_flush(self):
        if self.flush()[0] and self.straight()[0]:
            return True, self.sort_hand[0]
        return False, 0

    def royal_flush(self):
        return self.flush()[0] and sorted(self.sort_hand) == list(range(10, 15)), self.sort_hand[0]

    
    def compare(self):
        pass

    
    # Makes the cards look pretty
    def prettify(self, card):
        self.card = card
        return "[" , str(self.CARD_VALUES[self.card[0]]), self.CARD_SUITS[self.card[1]], "]"

    # Takes cards passed to it
    # Passes through prettify function
    # Returns pretty cards
    def print_cards(self, cards):
        self.cards = cards
        return ''.join([''.join(self.prettify(card)) for card in self.cards])

    def print_cards2(self, cards):
        self.cards = cards
        UNICODE_CARDS = {
            '🂡': 'AS',
            '🂱': 'AH',
            '🃁': 'AD',
            '🃑': 'AC',
            '🂢': '2S',
            '🂲': '2H',
            '🃂': '2D',
            '🃒': '2C',
            '🂣': '3S',
            '🂳': '3H',
            '🃃': '3D',
            '🃓': '3C',
            '🂤': '4S',
            '🂴': '4H',
            '🃄': '4D',
            '🃔': '4C',
            '🂥': '5S',
            '🂵': '5H',
            '🃅': '5D',
            '🃕': '5C',
            '🂦': '6S',
            '🂶': '6H',
            '🃆': '6D',
            '🃖': '6C',
            '🂧': '7S',
            '🂷': '7H',
            '🃇': '7D',
            '🃗': '7C',
            '🂨': '8S',
            '🂸': '8H',
            '🃈': '8D',
            '🃘': '8C',
            '🂩': '9S',
            '🂹': '9H',
            '🃉': '9D',
            '🃙': '9C',
            '🂪': 'TS',
            '🂺': 'TH',
            '🃊': 'TD',
            '🃚': 'TC',
            '🂫': 'JS',
            '🂻': 'JH',
            '🃋': 'JD',
            '🃛': 'JC',
            '🂭': 'QS',
            '🂽': 'QH',
            '🃍': 'QD',
            '🃝': 'QC',
            '🂮': 'KS',
            '🂾': 'KH',
            '🃎': 'KD',
            '🃞': 'KC'
        }
        REVERSE_UNICODE_CARDS = {v:k for (k,v) in UNICODE_CARDS.items()}
        # print(UNICODE_CARDS)
        return ' '.join([REVERSE_UNICODE_CARDS[card] for card in self.cards])