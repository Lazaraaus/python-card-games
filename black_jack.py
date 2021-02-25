from card_suite import Card, Deck 
from card_player import CardPlayer, CardDealer
from card_game import CardGame, BlackJackGame 

print("\nLet's play a game of Black Jack")
print("\nFirst you need to enter how many players")
n_players = int(input("\nEnter number of players: "))

print("\nNow we will need to input the names for the players")
p_names = []
while n_players != 0:
	p_names.append(input("\nPlease enter a name for player: "))
	n_players -= 1

players = []
count = 1
for name in p_names:
	players.append(CardPlayer(name, count))
	count += 1

game = BlackJackGame(players)

n_players = game.num_players


# game.Players()
# game.Start()

card = Card('Ace', 'Heart')
card2 = Card('2', 'Heart')
card3 = Card('6', 'Spade')
card4 = Card('10', 'Club')
card.PrintCard()
card2.PrintCard()
card3.PrintCard()
card4.PrintCard()

# aces = {}

# for player in players:
# 	player.GetCard(card2)
# 	player.GetCard(card3)
# 	player.GetCard(card)

# for player in players:
# 	aces[player] = game.ContainsAce(player)

# for player in players:
# 	print(aces[player])
