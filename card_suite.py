#Python Class to simulate a suite of cards
import random
from random import shuffle

#Global TODO: Add error catching blocks (built-in and self-defined) to all critical functions
#Global TODO: Add unit tests for all classes and functions 

#Utility function to return list of RANKS
def RANKS(): return ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 
				'Ace']
#Utility function to return list of SUITS
def SUITS(): return ['Heart', 'Diamond', 'Spade', 'Club']

#Class definition for Card
class Card:
	"""A simple attmept to model a Card class"""
	def __init__(self, rank, suit):
		"""Initializes Card Class"""
		self.rank = rank
		self.suit = suit
		self.value = 0
		self.converted = False 

	def __str__(self):
		"""Private function called when a Card is printed"""
		return self.rank.title() + " of " + self.suit.title() + "'s" 

	def PrintCard(self):
		"""Function to print formatted information about the card"""
		print(f"\n{self.rank.title()} of {self.suit.title()}'s")

	def ReturnCard(self):
		"""Function to return the formatted information as a string"""
		formatted_info = f"{self.rank.title()} of {self.suit.title()}'s"
		return formatted_info

#Class definition for Deck
class Deck:
	"""A simple attempt to model a Deck class"""
	def __init__(self):
		"""Initializes the Deck class"""
		self.contents = [Card(rank, suit) for rank in RANKS() for suit in SUITS()]
		random.shuffle(self.contents)

	def PrintDeck(self):
		""""Prints the current contents of the Deck"""
		for content in self.contents:
			print(content)

	def PopCard(self):
		"""Removes one card from the Deck"""
		return self.contents.pop()
	
	def ShuffleDeck(self):
		"""Shuffles the deck"""
		random.shuffle(self.contents)

	def CutDeck(self):
		"""'Cuts' the deck, as traditional in competitive card games"""
		tmp_str = self.contents[27:]
		self.contents[27:] = self.contents[:26]
		self.contents[:26] = tmp_str

	def DeckSize(self):
		"""Returns the size of the deck"""
		return len(self.contents)

	def DeckEmpty(self):
		"""Returns true if the Deck is empty, false otherwise"""
		if len(self.contents) == 0:
			return True 
		else:
			return False 

	def PeekDeck(self):
		"""Peek at the top of the deck"""
		self.contents[-1].PrintCard()






