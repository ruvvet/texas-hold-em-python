from cards import Cards
from utils import input_num, input_str

RAISE_AMT = 'Raise: $'
INPUT_ERROR_INT = 'Must be an integer. Try again.'
INPUT_ERROR_STR = 'Must be either K, C, R, F. Try again.'
PLAYER_ACTION = 'Chec[K], [C]all, [R]aise, [F]old: '
NO_CHECK_ERROR = ' - - Cannot Chec[K]. [C]all, [R]aise, or [F]old.'
PLAYER_FOLD = 'You have folded.'
PLAYER_MATCH = 'You have matched the bet: $'
PLAYER_RAISE = 'You have raised the bid to: $'
FUNDS_LOW_ERROR = 'Insufficient funds.'


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
    def player_summary(self, player, bet_round):
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
                player_history = self.history[bet_round] if bet_round in self.history else []

                )
            )