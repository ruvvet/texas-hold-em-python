import random

# Strings
NUM_PLAYERS = 'How many players?:   '
BLIND = 'Little Blind: $  '
START_AMT = 'Starting funds for each player: $  '
RAISE_AMT = 'Raise: $'
INPUT_ERROR_INT = 'Must be an integer. Try again.'
INPUT_ERROR_STR = 'Must be either K, C, R, F. Try again.'
PLAYER_ACTION = 'Chec[K], [C]all, [R]aise, [F]old: '
NO_CHECK_ERROR = ' - - Cannot Chec[K]. [C]all, [R]aise, or [F]old.'

GAME_START = '🎲-GAME START-🎲'
ROUND_START = '🎲-STARTING A NEW ROUND-🎲'
DEALING_PLAYER_CARDS = '...Dealing cards to players...'
PLAYER_FOLD = 'You have folded.'
PLAYER_MATCH = 'You have matched the bet: $'
PLAYER_RAISE = 'You have raised the bid to: $'
WIN_BY_FOLD = '...ONE PLAYER LEFT...'

FUNDS_LOW_ERROR = 'Insufficient funds.'
UPDATING = 'Updating Winner(s) Funds. Preparing for next round.'
FILLER = '...'


# Input validation
def input_num(message):
    while True:
        try:
            user_input = int(input(message))
        except ValueError:
            print(INPUT_ERROR_INT)
            continue
        else:
            return user_input
            break

def input_str(message):
    while True:
        try:
            user_input = str(input(message).upper())
            if user_input not in ['K','C', 'R', 'F']:
                raise ValueError
        except ValueError:
            print(INPUT_ERROR_STR)
            continue
        else:
            return user_input
            break


# Main Class
#   Starts the game
#   Asks basic input (# of players, big blind, start funds)
#   Manages + creates other classes
#       Board, Deck, Players, Community
#   Manages multiple rounds
#   Determines the final winner
class Texas_hold_em:

    def __init__(self):
        # Call main function
        self.main()
        self.final_winner = False

    def main(self):
        print("♤ ♧ ♡ ♢ TEXAS HOLD 'EM ♤ ♧ ♡ ♢")
        # Get input for number of players, big blind, start funds
        self.n = input_num(NUM_PLAYERS)
        self.blind_amt = input_num(BLIND)
        self.start_amt = input_num(START_AMT)

        print('\n {:^26}'.format(GAME_START))

        # Create a deck
        self.deck = Deck()

        # Create Community class
        # Pass arguments:
        #   Deck - to draw cards
        self.community = Community(self.deck, self.blind_amt)

        # Make the number of player classes needed based on input
        # Use a dictionary to name them via keys
        #   Dict key = player name
        #   Dict value = instance of class Player
        # Pass as arugments:
        #   start funds - to get start amount of $
        #   deck - to draw cards
        #   big blind
        #   community - to get check state, raise amount
        self.players = {x+1:Player(self.start_amt, self.deck, self.blind_amt, self.community) for x in range(self.n)}
        
        # Make a dealer class to handle who is the dealer
        # Takes the players, blind, and community classes as arguments        
        self.dealer = Dealer(self.players, self.blind_amt, self.community)

        # new players dictionary is ordered by order
        self.players = self.dealer.bet_order()

        # Create the board
        # Pass as arugments:
        #   Players
        #   Community
        self.board = Board(self.players, self.community, self.dealer)




        while self.check_final_winner(self.players) == False:




            print('players still in the game', ','.join([str(player_num) for player_num, player in self.players.items() if player.funds > (self.blind_amt*2)]))
            self.players = {player_num: player for player_num, player in self.players.items() if player.funds > (self.blind_amt*2)}
            self.check_final_winner(self.players)

            # Update dealer
            self.dealer.dealer = (self.dealer.dealer + 1) % len(self.players)

            # start next round
            print('\n' + ROUND_START +'\n'+ DEALING_PLAYER_CARDS)
            board = Board(self.players, self.community, self.dealer)
            

        print ('\n PLAYER {winner} wins it all!'.format(winner = [player_num for player_num, player in self.players.items()][0]))


    # check for final winner?
    # if everyone else has 0 funds
    # should return true if there is only 1 player left
    def check_final_winner(self, players_still_playing):
        #return len([player.funds for player_num, player in self.players.items() if player.funds >0]) == 1

        if len(players_still_playing) == 1:
            print ('PLAYER {winner} wins it all!'.format(winner = [player_num for player_num, player in players_still_playing.items()][0]))
            return True

        return False
        #return len(players_still_playing) == 1



# Board class
#   Manages printing the state of the game
#   Manages the betting + drawing rounds
#   Manages the winner of a round
class Board:

    def __init__(self, players, community, dealer):
        self.players = players
        self.community = community
        self.round_counter = 0
        self.round_winner = False
        self.dealer = dealer
        self.dealer.set_blinds()
        self.rounds()
        


    # Print board and update/reset variables
    def print_board(self):
        
        # Prints after the each betting round is complete
        # Prints Player (#, cards, funds, player call)
        # player call (unnecessary with the conditions added later)
        print('\n OVERVIEW (maybe take this out later?)')
        for player_num, player in self.players.items():
            print(
                'PLAYER {player_num} : {player_cards}' \
                ' >> $: {player_funds}' \
                ' >> Position: {player_position}' \
                ' >> Action: {player_action}'.format(
                player_num = player_num, 
                player_cards = player.player_cards, 
                player_funds = player.funds,
                player_position = player.player_position(),
                player_action = player.player_call
                )
            )
            print('bet', player.bet_amt)
        # Print the pot
        print('💰 POT: $ {pot}'.format(pot = self.community.pot))
        # Reset check state
        self.community.check = True
        # Reset amt needed to match
        self.community.match_raise = 0

    # Manages betting and drawing rounds
    def rounds(self):
        
        # List of the betting rounds
        self.bet_round = ['Pre-flop Betting', '2nd Betting', '3rd Betting', '4th Betting']
        # Dict of draw rounds with # of cards drawn for each
        self.draw_round = {'Flop': 3, 'Turn':1, 'River':1, 'Showdown':0}
        # List of the draw round keys to get the names of the rounds
        self.draw_key = list(self.draw_round.keys())

        # While counter is under 5
        # Keep adding to counter and increasing round #
        while self.round_counter < 4:
            # Print the betting round
            print('\n ⌛ BETTING ROUND: {bet_round}'.format(bet_round = self.bet_round[self.round_counter].upper()))
            # Call the betting round function
            self.start_betting(self.bet_round[self.round_counter])

            # Cnce betting round is over and everyone has folded/matched
            # Print draw round
            # Draw community cards - draw n cards by looking up the values in the draw_round dictionary
            # Print community cards
            print('\n ⚡ DEAL: {deal_round}'.format(deal_round = self.draw_key[self.round_counter].upper()))
            self.community.community_hand(self.draw_round.get(self.draw_key[self.round_counter]))
            print('COMMUNITY CARDS: {uni_cards} {pretty_cards}'.format(
                uni_cards = self.community.cards.print_cards2(self.community.comm_cards),
                pretty_cards = self.community.cards.print_cards(self.community.comm_cards)
                )
            )
            self.check_for_winner(self.round_counter)
            self.print_board()
            self.round_counter += 1

        # else evaluate cards goes here*

    # Manages betting
    def start_betting(self, betting_round):
        # For each player
        # Print player #, cards, funds
        # Call player_state function, and check their call to update check state



        # is there a way to remove this section and have it all under the while loop?
        # When i try it gives a no attribute error since it seems to  try to call the player calls when they dont yet exist?


        for player_num, player in self.players.items():
            # Calls player summary 
            player.player_summary(player_num)
            #print('Hand Strength: ', player.hand_strength())
            # Call player_state func, then pass the player_state into check function to update check state
            #player.player_state(self.community.can_check())


    # round 2 where i pass it 3x to get player history
            player.player_history(player.player_state(self.community.can_check()), betting_round)

        # Every player must either fold or match the highest bet in order to move to the next round
        # If all player bet_amts are not equal to the highest raise
        # Continue prompting input
        while list(set([player.bet_amt for player_num, player in self.players.items() if player.player_cards != []]))[0] != self.community.match_raise:

            #print(list(set([player.bet_amt for player_num, player in self.players.items() if player.player_call != 'F']))[0])
            print('All remaining player bets must match the current high bet. \n Amount to match: ${match}'.format(match=self.community.match_raise), 
                '\n [C]all, [R]aise, or [F]old')

            for player_num, player in self.players.items():
                if player.player_call != 'F' and player.bet_amt < self.community.match_raise:
                    player.player_summary(player)
                    #player.player_state(self.community.can_check())
                    player.player_history(player.player_state(self.community.can_check()), betting_round)

        # Update everyone's funds here outside of the loop once betting is all complete
        # Update community pot here

        for player_num, player in self.players.items():
            player.player_funds(player.bet_amt)
            self.community.update_pot(player.bet_amt)
            # reset bet amt for round to 0
            player.bet_amt = 0

    def check_for_winner(self, round_counter):
        # print(len([player.player_call for player_num, player in self.players.items() if player.player_call == 'F']))
        # print(len(self.players.keys())-1)

        self.WINNER = {player_num: player for player_num, player in self.players.items() if player.player_cards != []}
        #self.still_playing = [player_num for player_num, player in self.players.items() if player.player_call != 'F']
        if len(self.WINNER) == 1:
            self.round_winner = True
            print('\n' + WIN_BY_FOLD)
            #self.WINNER = self.still_playing            
        # i thought maybe it wasn't working since there weren't enough cards and it was giving a list index out of range error
        if round_counter == 3:
            # What happens when somebody folds?
            self.round_winner = True
            self.FINAL_HANDS = {player_num: player.full_hand() for player_num, player in self.players.items()}
            self.WINNER = self.evaluate_winning_hand(self.FINAL_HANDS, 0)
            #self.player_round_winner = [k for k,v in self.WINNER_HAND.items()]
        self.declare_winner(self.WINNER)



    # Evaluates the winning hand
    # Takes the dictionary of all the final full hands
    # Steps through each index using a counter
    # Replaces old dictionary only with hands who have the greatest value at that index
    # Move onto next index with reduced dictionary
    # Rinse and repeat
    def evaluate_winning_hand(self, FINAL_HANDS, counter):
        if len(FINAL_HANDS.keys()) == 1 or counter > 7:
            return FINAL_HANDS
        else:
            self.zipped = list(zip(*FINAL_HANDS.values()))
            FINAL_HANDS = {k:v for k,v in FINAL_HANDS.items() if v[counter] >= max(self.zipped[counter])}
            return self.evaluate_winning_hand(FINAL_HANDS, counter +1)

    # Declares the winner
    # Takes dictionary input
    # Should have either tied hands or just the winning hand

    # THIS PART IS SUPER CRAZY AND I DONT LIKE IT

    # 1. Prints all the players who are still left in the 'final winners' dictionary if there are more than 2
    # 2. else there is only one winner

    def declare_winner(self, WINNER):
        if self.round_winner:
            if len(WINNER) > 1:
                print('\n Tie between players', ' & '.join(['{}']*len(WINNER.keys())).format(*WINNER.keys()))
                # divide pot among winning players
                print()
                for p in list(WINNER.keys()):
                    self.players[p].funds += self.community.pot/len(WINNER)
            else:
            
                print('\n 🎉🎉🎉 Player {} wins!'.format(*WINNER.keys()))
                # wtf am i doing here
                for player_num, players in self.players.items():
                    for x in WINNER.values():

                        # ISSUE - if they won due to a kicker and not the best hand type, this statement is untrue because it doesnt evaluate if they won due to a kicker or not.
                        self.winning_hand = [players.cards.RANKED_HAND_TYPES[x[0]] for x in WINNER.values()][0]
                        self.winning_card = [players.cards.REVERSE_CARD_VALUES[x[1]] for x in WINNER.values()][0]
                print('Winning hand: {hand_type} with {card}.'.format(hand_type = self.winning_hand, card = self.winning_card))

                # update player funds with whole pot
                self.players[list(self.WINNER.keys())[0]].funds += self.community.pot
                # empty pot
                self.community.pot = 0
                # reset community hand
                self.community.comm_cards = []
            
            print('\n' + UPDATING,
            '\n' + FILLER,
            '\n' + FILLER,
            '\n' + FILLER)



# Deck Class
#   Manages the deck of cards
#   Is called whenever a card/s is drawn
#   Keeps track of deck "order", which cards are in play, and which cards remain
#   Deals from top/beginning of the list to players/table
class Deck:

    def __init__(self):
        self.deck_val = '23456789TJQKA'
        self.deck_suit = 'CDHS'
        # Make the full 52 card deck
        self.full_deck = [''.join([val,suit]) for suit in self.deck_suit for val in self.deck_val]
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

# Player Class
#   One instance for each player
#   Tracks all variables related to individual player
#       2 cards
#       Funds
#       Betting state
#       player call history
#       player position
class Player:

    def __init__(self, funds, deck, blind, community):
        self.funds = funds
        self.player_cards = []
        self.deck = deck
        self.community = community
        self.bet_amt = 0
        self.cards = Cards(self.player_cards + self.community.comm_cards)
        self.player_hand()
        self.history = {}
        self.blind_amt = blind
        self.is_dealer = False
        self.is_big_blind = False
        self.is_little_blind = False

# Input validation to make sure they arent betting more $ than they have available
    def input_money(self, message):
        while True:
            try:
                user_input = int(input(message))
            except ValueError:
                print(INPUT_ERROR_INT)
                continue
            if user_input > self.funds:
                print(FUNDS_LOW_ERROR)
                continue
            else:
                return user_input
                break


    # Draws 2 cards for player
    # If they still have money to play
    def player_hand(self):
        if self.funds > 0:
            for card in self.deck.draw(2):
                self.player_cards.append(card)

    # Updates players funds once bet is finalized
    def player_funds(self, bet_amt):
        self.funds -= bet_amt
        return self.funds

    # The total amount that has been bet the entire game
    def total_bet(self, bet_amt):
        self.total_bet_amt = []
        self.total_bet_amt.append(bet_amt)
        return sum(self.total_bet_amt)


    # Prompts input for bet state
    def player_state(self, check):

        # If player's hand is empty, they have folded and cannot participate this match
        if not self.player_cards:
            print(PLAYER_FOLD)
        else:
            self.player_call = input_str(PLAYER_ACTION).upper()

            # If player folds, hand is discarded
            if self.player_call == 'F':
                self.player_cards = []
            # If player checks, they make no bets
            # Can only check if no bets are made
            elif self.player_call == 'K' and not check:
                print(NO_CHECK_ERROR)
                return self.player_state(check)
            # If player raises, everyone else mutch match or re-raise
            elif self.player_call == 'R':
                print(' - - Raise the current high bet (${bet}) for this round. (Your bets this betting round/Total chips on the table: ${current_bet}/${total_bet}).'.format(

                    bet = self.community.match_raise,
                    current_bet = self.bet_amt,
                    total_bet = self.total_bet(self.bet_amt)
                    )
                )
                self.bet_amt = self.input_money(RAISE_AMT) + self.community.match_raise
                
                # !!! Set it to that 'Raise' always is added to the current highest bid.
                # Circumvents the issue of needing a check
                
                
                # print('raised bet', self.bet_amt)
                # self.bet_diff = abs(self.community.match_raise - self.bet_amt) + 1
                
                # # If player wants to raise, must be greater than current highest raise
                # while self.bet_amt <= self.community.match_raise:
                #     print('Bet ${diff} more to raise the current high bet of ${bet}.'.format(
                #         diff = self.bet_diff,
                #         bet = self.community.match_raise
                #         )
                #     )
                #     self.bet_amt += input_num('RAISE AMT OF MY BET BY $:')
                # If the raise if valid, subtract player funds, add to pot
                #if self.bet_amt > self.community.match_raise:
                self.community.match_raise = self.bet_amt
                print(PLAYER_RAISE+'{raise_amt}. High bid is now: ${bet}.'.format(
                    raise_amt = self.bet_amt,
                    bet = self.community.match_raise
                ))
                    

                    # self.player_funds(self.bet_amt)
                    # self.community.update_pot(self.bet_amt)
            # If player calls, they make a bet equal to the current highest bet
            # Subtract from funds and update pot accordingly
            elif self.player_call == 'C':
                if self.community.match_raise > self.funds:
                    print(FUNDS_LOW_ERROR)
                    return self.player_state(check)
                else:
                    self.bet_amt = self.community.match_raise
                    # self.player_funds(self.community.match_raise)
                    # self.community.update_pot(self.community.match_raise)
                    print(PLAYER_MATCH, self.community.match_raise)
                


            return self.player_call

    # there is probably a better way to do this??
    # Determines how much blind each player has to give if they are the big/little blind
    def player_position(self):
        if self.is_dealer == True:
            return 'Dealer'
        elif self.is_big_blind == True:
            return 'Big Blind (${blind})'.format(blind = str(self.blind_amt*2))
        elif self.is_little_blind == True:
            return 'Little Blind (${blind})'.format(blind = str(self.blind_amt))

        return ' '

    def full_hand(self):
        self.hand_str = self.cards.get_hand(self.player_cards, self.community.comm_cards)
        return self.hand_str

    def player_history(self, call, bet_round):
        # Create a dictionary with key as round, calls as list for values
        self.history.setdefault(bet_round, [])
        self.history[bet_round].append(call)


        
    # Player summary that is called during each betting around
    # Placed here to prevent reptition when it is needed    
    def player_summary(self, player):
        print('\n >> Turn : PLAYER {player_num} // {player_position}' \
            '\n >> Your Cards: {uni_cards} {cards}' \
            '\n >> Your Funds: ${player_funds}' \
            '\n >> Current Bet: ${player_bet}' \
            '\n >> Player History: {player_history}'.format(
                player_num = player,
                player_position=self.player_position(), 
                uni_cards = self.cards.print_cards2(self.player_cards),
                cards=self.cards.print_cards(self.player_cards),
                player_funds=self.funds,
                player_bet=self.bet_amt,
                # issues with calling the bet round because player_history function has not yet
                # been called, so calling specific values in the dict gives an error
                player_history = self.history

                )
            )


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



poker = Texas_hold_em()


#TO DO:

# hand strength probabilities (bitwise method?)
# continue making new rounds until one player has most of the money (other players do not have enough for big blind)
# all in
# compartmentalize into separate modules



# person after big blind always goes first - done
## fix the fucked up betting amounts - done (was performing redundant actions after bet_amt was initialized with blind amt)
# # initialize current bet with big blind - done


# List of issues to fix:
# getting the specific round's history for each player
