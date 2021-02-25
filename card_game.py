#Python Class for representing Card Games and Card Game logic
from card_suite import Card, Deck
from card_player import CardPlayer, CardDealer 

#Global TODO: Add error catching blocks (built-in and self-defined) to all critical functions
#Global TODO: Add unit tests for all classes and functions 

class CardGame:
	"""A Simple class for modeling a card game"""
	def __init__(self, players):
		"""Function to initialize a Card Game"""
		
		#instantiate a dealer for the game
		self.dealer = CardDealer() 

		#Builds the player list in the dealer object and then 
		#Gives the game object a list of the players who started the game
		self.dealer.BuildPlayersList(players)
		self.game_players = self.dealer.GetPlayersList()
		self.num_players = len(self.game_players) - 1

		#Boolean attribute for game over check
		self.game_over = False
		#Int attribute for keeping track of the number of rounds
		self.num_rounds = 0
		#Dict to map value of cards to rank
		self.value_chart = {}

	def GameOver(self, bool_value):
		"""Function to set attribute_game to bool_value"""
		self.game_over = bool_value 

	def Deal(self, num_cards):
		"""Function to deal a specific number of cards to each player"""
		self.dealer.DealCards(num_cards)

	def Players(self):
		"""Function to print all players in the current game"""
		self.dealer.PrintPlayersList()

	def PlayerCount(self):
		"""Function to return number of players"""
		print(f"\nThe number of players is: {self.num_players}")

	def CardsLeft(self):
		"""Function to check how many cards are left in this game's deck"""
		return self.dealer.deck.DeckSize()
	
	def Peek(self, player):
		"""Function to allow a player to peek at their last card"""
		player.PeekHand()

	def CardPosition(self, player, card, card_rank=0, card_suite=0):
		"""Function to return the position of a Card in a players Hand"""
		#TODO-CardPosition check using rank and suite
		if card_rank & card_suite == 0:
			position = player.hand.index(card)
			return position 

class BlackJackGame(CardGame):
	"""A child class of CardGame modeling BlackJack"""
	def __init__(self, players):
		"""Function to initialize a BlackJackGame class"""

		#Call parent constructor
		super().__init__(players)

		#Set value_chart
		self.value_chart = {'2' : 2,
							'3': 3,
							'4': 4,
							'5': 5, 
							'6': 6,
							'7': 7,
							'8': 8,
							'9': 9,
							'10': 10,
							'Jack' : 10,
							'Queen': 10,
							'King': 10,
							'Ace': 11
							}

		#Dictionary to track all info about Player
		#TODO - Eventually move into Django ORM database
		self.players_info = {}

		#TODO - JSON file for rules, to allow specific rule sets
		#TODO - Function (exit?) to check if players want to quit and cash out their earnings or keep playing 
		#TODO - BuyBack function for players who have negative player scores at the start of a round 
		#TODO - Boolean functions for PlayerBust, PlayerBlackJack, PlayerPush to clean up Payout() and Pay()

#-----------Internal Methods---------------
	#-------Setters & Getters--------------
	def SetValues(self):
		"""Function to set each card in the Dealer Deck to the correct value"""
		self.dealer.EditValues(self.value_chart)

	def SetInfo(self):
		"""Function to set player_info dict to initial values"""
		#TODO - condense player_won, player_push into player_outcome
		for player in self.game_players:
			self.players_info[player] = {'hand_value': player.GetHandValue(),
											'player_bust': False,
											'black_jack': False,
											'choice_list': ['hit', 'double', 
															'stand', 'split'],
											'player_won': False,
											'player_payout': False,
											'player_push': False,
											'player_bet': 0,
											'player_score': player.GetScore(),
											}

	def UpdateHandValue(self, player):
		"""Function to update a single players hand value in the players_info
		 dict""" 
		self.SetPlayerInfo(player, 'hand_value', player.GetHandValue())

	def UpdateHandValues(self):
		"""Function to update all the hand values for all the players in the
		players_info dict"""
		for player in self.game_players:
			self.UpdateHandValue(player)

	def HandValue(self, player):
		"""Function to return a single player's hand value"""
		return self.GetPlayerInfo(player, 'hand_value')
	
	def PrintHand(self, player):
		"""Function to display the hand of a player"""
		if player in self.game_players:
			player.ShowHand()
		else:
			print("That player doesn't exist")

	def PrintInfo(self, player):
		print(f"\n{player.username} it's your turn")
		print("\nCurrent hand is: ")
		self.PrintHand(player)
		print("\nCurrent hand value is:")
		print(self.HandValue(player))

	def GetPlayerInfo(self, player, info): 
		"""Function to get specific (info) fields of players_info dictionary"""
		return self.players_info[player][info]

	def SetPlayerInfo(self, player, info, value):
		"""Function to set specific (info) fields of players_info dictionary"""
		self.players_info[player][info] = value 

	#---------Black Jack Game Methods------------------
	def Deal(self, num_cards=1):
		"""Function to deal 1 Card to each player and updates Hand Values"""
		print("\nDealing cards...")
		self.dealer.DealCards(num_cards)

	def BlackJack(self, player):
		"""Function to check if Player has BlackJack. Sets the black_jack field 
		in the players_info dictionary to True"""
		if self.HandValue(player) == 21 and player.hand_length == 2:
			self.SetPlayerInfo(player, 'black_jack', True)
			print(f"Congratulations {player.username} you have BlackJack")

	def Hit(self, player):
		"""Function to model a 'Hit' in BlackJack"""

		#Dealer
		if player == self.game_players[-1]:
			#Deal card and update dealer's hand value
			self.dealer.DealCard(player)
			self.UpdateHandValue(player)

			#Print message and contents of Card 
			print(f"\nPlayer {player.username} has been hit with: ")
			player.DisplayCard(-1)

			#If Dealer Busts and Has an Ace, Convert it. 
			if self.HasBust(player) and len(self.ContainsAce(player)) != 0:
				self.Convert(player)
			
			else:
				#Print Dealer info and continue Dealer turn 
				self.PrintInfo(player)
				self.EndRound()

		#Normal player
		else:
			#Deal card and update player's hand value
			self.dealer.DealCard(player)
			self.UpdateHandValue(player)
		
			#Print message and contents of Card 
			print(f"\nPlayer {player.username} has been hit with: ")
			player.DisplayCard(-1)

			#Check if player was hit with an Ace
			self.Convert(player)

			#Check for Bust
			if self.HasBust(player) == False:
				self.PrintInfo(player)
				self.Choice(player)
			else:
				self.Bust(player)

	def Stand(self, player):
		"""Function to model a Stand in Black Jack"""
		print(f"Player {player.username} has chosen to Stand")
	
	def Choice(self, player):
		"""Function to handle Player choice: Hit, Stand, Convert, Split, Double
		Down, etc. 
		"""
		#Main choice logic TODO - Implement Split and Double Down
		print("\n What would you like to do? ")
		print("\n Type for choice: ")
		print("\n\t Hit (hit)")
		print("\t Stand (stand)")
		print("\t Double Down (double)")
		print("\t Split (split)")
		choice_cmd = input("\nChoice: ")
		if choice_cmd.lower() in self.players_info[player]['choice_list']:
			if choice_cmd.lower() == 'hit':
				self.Hit(player)

			elif choice_cmd.lower() == 'stand':
				self.Stand(player)

			elif choice_cmd.lower() == 'double':
				print(f"{player.username} has chosen to double")

			elif choice_cmd.lower() == 'split':
				print(f"{player.username} has chosen to split")

	def Bet(self):
		"""Function to model a Player making a Bet"""
		#TODO - Legal Bet Check, make sure they have enouch 'score' to bet
		#Ask player for bet
		for player in self.game_players[:self.num_players]:
			print(f"\n{player.username} please make a wager")
			bet = input(f"\n\t{player.username}'s wager: ")
			
			#Record Bet into players_info
			self.SetPlayerInfo(player, 'player_bet', bet)

	#---------Bust Methods--------------------------------
	def Bust(self, player):
		"""Function to remove a player who has gone Bust"""
		#Print Bust message
		print(f"\nPlayer {player.username} has bust with {self.HandValue(player)}!")
		
		#Set Player value for player_bust in players_info to True
		self.SetPlayerInfo(player, 'player_bust', True)

	def HasBust(self, player):
		if self.HandValue(player) > 21:
			return True
		else:
			return False
			
	#---------Ace Conversion Methods-------------------------
	def Convert(self, player):
		"""Function to handle Ace conversion"""
		#Dealer 
		if player == self.game_players[-1]:
			ace_positions = self.ContainsAce(player)
			if len(ace_positions) != 0:
				for ace_position in ace_positions:
					#If been converted - do nothing
					if self.IsConverted(player.hand[ace_position]):
						pass
					#If not converted - convert
					else: 
						print("\nConverting Dealer Ace('s)")
						self.ConvertAce(player, ace_position)
				self.PrintInfo(player)
				self.EndRound()

		#Normal Player
		else:
			ace_positions = self.ContainsAce(player)
			if len(ace_positions) != 0:
				for ace_position in ace_positions:
					print("\nWould you like to convert your Ace?")
					print(f"\nThe value of your Ace is: {player.hand[ace_position].value}")
					convert_cmd = input("\n (yes)/(no) ")
					if convert_cmd.lower() == 'yes':
						self.ConvertAce(player, ace_position)
						#Print info about current hand value post-conversion
						self.PrintInfo(player)

	def ContainsAce(self, player):
		"""Function to return a list of card positions of Ace's""" 
		aces_positions = []
		if player.hand_length == 0:
			return aces_positions 
		else: 
			for card in player.hand:
				if card.rank == 'Ace':
					aces_positions.append(player.hand.index(card))
			return aces_positions 

	def ConvertAce(self, player, card_position):
		"""Converts Ace at card_position to 1 or 11 and then Updates Hand Value"""
		if player.hand[card_position].value == 1:
			player.hand[card_position].value = 11
			self.UpdateHandValue(player)
			player.hand[card_position].converted = False
			print(f"Value of Ace is now: {player.hand[card_position].value}")

		elif player.hand[card_position].value == 11:
			player.hand[card_position].value = 1
			self.UpdateHandValue(player)
			player.hand[card_position].converted = True
			print(f"Value of Ace is now: {player.hand[card_position].value}")

	def IsConverted(self, card):
		"""Function to check if an Ace has been converted"""
		return card.converted 

	def ConvertBust(self, player):
		#TODO MAJOR
		"""Function to check if Conversion will Bust dealer"""
		curr_hand_value = self.HandValue(player)
		#curr_ace_value = 

	#---------Methods for BlackJack Round-------------------------
	def EndRound(self):
		"""Function to model the end of a round"""
		#Get dealer object
		dealer_o = self.game_players[-1]
		#Check for BlackJack
		self.BlackJack(dealer_o)

		#TODO - Check for Pocket Aces
			#If Pocket Aces - Convert one
			#Else - Continue 

		#Check Dealer Score for Dealer Move
		if self.GetPlayerInfo(dealer_o, 'black_jack') == True:
		#Dealer has Blackjack, initiate Payout Logic
			self.Payout()

		elif self.HasBust(dealer_o) == False and self.HandValue(dealer_o) < 17:
		#Hand Value less than 17 - Hit Dealer
			self.Hit(dealer_o)

		elif self.HasBust(dealer_o) == False and self.HandValue(dealer_o) == 17:
		#Hand Value equal to 17 - Check for Ace to Convert
			#No ace - dealer Stands
			if len(self.ContainsAce(dealer_o)) == 0:
				self.Stand(dealer_o)
				#Payout Logic
				self.Payout()
				
			#Ace - convert it	
			else:
				self.Convert(dealer_o)

		elif self.HasBust(dealer_o) == False and self.HandValue(dealer_o) > 17:
		#Hand Value greater than 17 - Dealer Stands
			self.Stand(dealer_o)
			self.Payout()

		elif self.HasBust(dealer_o) == True:
		#Dealer Busts on hand 
			self.Bust(dealer_o)
			#Payout Logic
			self.Payout()

	def Round(self):
		"""Function to model a Round of BlackJack"""
		#Print information about current round
		self.num_rounds += 1											
		print(f"\n\tRound {self.num_rounds}")   
		
		#Deal Cards
		self.Deal(2)

		#Update Player Hand Values to reflect Deal
		self.UpdateHandValues()	

		#Begin Round w/ 1st player
		for player in self.game_players[0:self.num_players]:
			#Print info about Player, Hand Value, Current turn 
			self.PrintInfo(player)

			#Check if player has BlackJack
			self.BlackJack(player)

			#Check for Aces, Convert Aces if wanted.
			self.Convert(player)

			#Main Choice Logic
			self.Choice(player)

		#Print Info about Dealer
		dealer_o = self.game_players[-1]
		self.PrintInfo(dealer_o)
		
		#Check if all players have Bust
		if self.AllBust():
			self.Payout()
		else:
			#Dealer Turn
			self.EndRound()

	def AllBust(self):
		for player in self.game_players[:self.num_players]:
			if self.GetPlayerInfo(player, 'player_bust') == False:
				return False 
		return True  

	def Payout(self):
		"""Function to model the end of a BlackJack game"""
		print("End of game")
		dealer_o = self.game_players[-1]

		#Check who has won, pushed, or lost and adjust payouts accordingly
		if self.GetPlayerInfo(dealer_o, 'player_bust') == False:	
		#Dealer isn't Bust
			for player in self.game_players[:self.num_players]:
				#Check if Player hasn't Bust and doesn't have BlackJack
				if self.GetPlayerInfo(player, 'player_bust') == False and self.GetPlayerInfo(player, 'black_jack') == False:
					#Check if Player Hand beats Dealer Hand
					if self.HandValue(player) > self.HandValue(dealer_o):
						#If so, set player_won to True
						self.SetPlayerInfo(player, 'player_won', True)
						self.SetPlayerInfo(player, 'player_payout', 'normal')

					#Check for a Push
					elif self.HandValue(player) == self.HandValue(dealer_o):
						#Check if Dealer has BlackJack
						if self.GetPlayerInfo(dealer_o, 'black_jack') == True:
							#If so, Player loses
							self.SetPlayerInfo(player, 'player_won', False)
						else:
							#Player pushes with Dealer
							self.SetPlayerInfo(player, 'player_push', True)
							self.SetPlayerInfo(player, 'player_payout', 'refund')
					
					#Else Player loses 
					else:
						#Set player_won to False
						self.SetPlayerInfo(player, 'player_won', False)

				#Check if player hasn't bust and does have BlackJack 
				elif self.GetPlayerInfo(player, 'player_bust') == False and self.GetPlayerInfo(player, 'black_jack') == True:
					
					#Check if Dealer has BlackJack
					if self.GetPlayerInfo(dealer_o, 'black_jack') == True:
						#Player Push with Dealer on double BlackJack
						self.SetPlayerInfo(player, 'player_push', True)
						self.SetPlayerInfo(player, 'player_payout', 'refund')
				
					#If Dealer doesn't have BlackJack
					else:
						self.SetPlayerInfo(player, 'player_won', True)
						self.SetPlayerInfo(player, 'player_payout', 'double')

		else:	
		#Dealer has Busted
			for player in self.game_players[:self.num_players]:
				#Check if player hasn't Bust and doesn't have BlackJack
				if self.GetPlayerInfo(player, 'player_bust') == False and self.GetPlayerInfo(player, 'black_jack') == False:
					self.SetPlayerInfo(player, 'player_won', True)
					self.SetPlayerInfo(player, 'player_payout', 'normal')

				#Check if player hasn't Bust and has BlackJack
				elif self.GetPlayerInfo(player, 'player_bust') == False and self.GetPlayerInfo(player, 'black_jack') == True:
					self.SetPlayerInfo(player, 'player_won', True)
					self.SetPlayerInfo(player, 'player_payout', 'double')

		#Initiate Pay Method			
		self.Pay()

	def Pay(self):
		"""Function to pay bets depending on the value of payout"""
		#Handle Bets and Payouts 
		for player in self.game_players[:self.num_players]:
			if self.GetPlayerInfo(player, 'player_bust') == False:
				#Player Pushed
				if self.GetPlayerInfo(player, 'player_push') == True:
					#Refund Bet and zero bet
					self.SetPlayerInfo(player, 'player_bet', 0)
					print(f"{player.username} has pushed and the bet is refunded")

				#Player Lost and loses bet
				if self.GetPlayerInfo(player, 'player_won') == False and self.GetPlayerInfo(player, 'player_push') == False:
					bet = int(self.GetPlayerInfo(player, 'player_bet'))

					#Zero out bet
					self.SetPlayerInfo(player, 'player_bet', 0)
				
					#Add bet to Dealer score, substract bet from Player score
					self.dealer.AddScore(bet)
					player.SubScore(bet)
					print(f"{player.username} has lost and forefeits {bet}")
				
				#Player Won
				if self.GetPlayerInfo(player, 'player_won') == True:
					#Player won with BlackJack
					if self.GetPlayerInfo(player, 'black_jack') == True:
						#Get Bet
						bet = int(self.GetPlayerInfo(player, 'player_bet'))

						#Calculate Payout (3:2) and add to player score 
						bet = ((3 * bet)/ 2)
						player.AddScore(bet)

						#Print Message to Player 
						print(f"{player.username} has won with BlackJack and will receive {bet} for payout")

					#Play won without BlackJack
					else:
						#Get Bet
						bet = int(self.GetPlayerInfo(player, 'player_bet'))

						#Calculate Payout (1:1) and add to player score
						player.AddScore(bet)

						#Print Message to Player 
						print(f"{player.username} has won and will receive {bet} for payout")
			
			elif self.GetPlayerInfo(player, 'player_bust') == True:
				#Players Bust and lose their bet
				bet = int(self.GetPlayerInfo(player, 'player_bet'))
				self.SetPlayerInfo(player, 'player_bet', 0)
				
				#Add bet to Dealer score, substract bet from Player score
				self.dealer.AddScore(bet)
				player.SubScore(bet)

				print(f"{player.username} went bust and forefeits {bet}")
	
	def HasDouble(self, player):
		"""Function to check if the first two cards are the same"""


#------------External Methods---------------
	def Start(self):
		"""Lets us know the game has started, initialize necessary components,
		and then start the game
		"""
		#Game Start message
		print("\nGame Starting")

		#Initialize Values
		self.SetValues()
		self.SetInfo()
		self.UpdateHandValues()

		#Initiate Betting
		self.Bet()

		#Initiate Round
		self.Round()



#TODO - Entire other Card Game classes
class PokerGame(CardGame):
	"""A child class of CardGame modeling Poker"""

class SpadesGame(CardGame):
	"""A child class of CardGame modeling Spades"""

class HeartsGame(CardGame):
	"""A child class of CardGame modeling Hearts""" 

class WarGame(CardGame):
	"""A child class of CardGame modeling I Declare War"""

