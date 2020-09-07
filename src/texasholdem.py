from board import Board
from deck import Deck 
from cards import Cards
from player import Player 
from community import Community 
from dealer import Dealer 
from utils import input_num, input_str


# Strings
NUM_PLAYERS = 'How many players?:   '
BLIND = 'Little Blind: $  '
START_AMT = 'Starting funds for each player: $  '
GAME_START = '🎲-GAME START-🎲'
ROUND_START = '🎲-STARTING A NEW ROUND-🎲'
DEALING_PLAYER_CARDS = '...Dealing cards to players...'




# Main Class
#   Starts the game
#   Asks basic input (# of players, big blind, start funds)
#   Manages + creates other classes
#       Board, Deck, Players, Community
#   Manages multiple rounds
#   Determines the final winner
class TexasHoldEm:

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
