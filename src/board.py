WIN_BY_FOLD = '...ONE PLAYER LEFT...'
UPDATING = 'Updating Winner(s) Funds. Preparing for next round.'
FILLER = '...'

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
            player.player_summary(player_num, betting_round)
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
                    player.player_summary(player_num, betting_round)
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