#Python class for a Player of our Card game

#Global TODO: Add error catching blocks (built-in and self-defined) to all critical functions
#Global TODO: Add unit tests for all classes and functions 

from card_suite import Deck 

class CardPlayer:
	"""A simple class for modeling a player to play cards"""

	def __init__(self, username, player_number, score=0):
		"""Initialize Player"""
		self.username = username
		self.player_number = player_number
		self.score = score

		self.hand = []
		self.hand_length = 0

	def __str__(self):
		return self.username + " as " + self.player_number + " playing " + game_type

	def GetUsername(self):
		return self.username

	def GetPlayerNumber(self):
		return self.player_number

	def GetScore(self):
		return self.score 

	def ShowScore(self):
		print(self.score) 

	def AddScore(self, points):
		self.score += points

	def SubScore(self, points):
		self.score -= points

	def PlayCard(self, index=0):
		return self.hand.pop(index)

	def GetCard(self, card):
		self.hand.append(card)
		self.hand_length += 1

	def ShowHand(self):
		if self.hand_length == 0:
			print("Hand is empty")
		else:
			for card in self.hand:
				card.PrintCard()

	def DisplayCard(self, card_position): 
		if card_position <= self.hand_length:
			self.hand[card_position].PrintCard()
		else:
			print(f"This card doesn't exist in {player.username}'s hand and can't be displayed")

	def PeekHand(self):
		if self.hand_length == 0:
			print("Hand is empty")

		else:
			self.hand[-1].PrintCard()

	def GetHandValue(self):
		sum = 0
		for card in self.hand:
			sum += card.value 
		return sum 

class CardDealer(CardPlayer):
	"""A simple child class  of CardPlayer to model a card game dealer"""
	def __init__(self, username='Dealer', player_number=0):
		"""Function to initialize Card Dealer class"""

		#Call parent constructor
		super().__init__(username, player_number)

		#Class attribute to store list of current players 
		self.player_list = []

		self.deck = Deck()

	def BuildPlayersList(self, players):
		for player in players:
			self.player_list.append(player)

		self.player_list.append(self)

	def GetPlayersList(self):
		return self.player_list

	def PrintPlayersList(self):
		for player in self.player_list:
			print(player.GetUsername()) 

	def RemovePlayer(self, player):
		self.player_list.remove(player)

	def GetPlayerScore(self, player):
		return player.GetPlayerScore()

	def PlayerAddPoints(self, player, points):
		player.AddScore(points)

	def PlayerSubPoints(self, player, points):
		player.SubScore(points)

	def DealCard(self, player):
		player.GetCard(self.deck.PopCard())

	def DealCards(self, num_cards):
		for player in self.player_list:
			for num in range(1, num_cards + 1):
				self.DealCard(player)

	def EditValues(self, value_dict):
		for card in self.deck.contents:
			card.value = value_dict[card.rank]




