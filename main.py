from random import shuffle
from time import sleep


class Card:

	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

	def __str__(self):
		return f"{self.rank['rank']} of {self.suit}"


class Deck:

	def __init__(self):
		self.cards = []
		suits = ["spades", "clubs", "hearts", "diamonds"]
		ranks = [
			{"rank": "A", "value": 11},
			{"rank": "2", "value": 2},
			{"rank": "3", "value": 3},
			{"rank": "4", "value": 4},
			{"rank": "5", "value": 5},
			{"rank": "6", "value": 6},
			{"rank": "7", "value": 7},
			{"rank": "8", "value": 8},
			{"rank": "9", "value": 9},
			{"rank": "10", "value": 10},
			{"rank": "J", "value": 10},
			{"rank": "Q", "value": 10},
			{"rank": "K", "value": 10},
		]

		for suit in suits:
			for rank in ranks:
				self.cards.append(Card(suit, rank))

	def shuffle(self):
		if len(self.cards) > 1:
			shuffle(self.cards)

	def deal(self, amount):
		cards_dealt = []

		for _ in range(amount):
			if len(self.cards) > 0:
				card = self.cards.pop()
				cards_dealt.append(card)

		return cards_dealt


class Hand:

	def __init__(self, dealer=False):
		self.cards = []
		self.dealer = dealer

	def add_card(self, card_list):
		self.cards.extend(card_list)

	def calculate_value(self):
		self.value = 0
		has_ace = False

		for card in self.cards:
			if card.rank["rank"] == "A":
				has_ace = True
			self.value += card.rank["value"]

		if has_ace and self.value > 21:
			self.value -= 10

	def get_value(self):
		self.calculate_value()
		return self.value

	def is_blackjack(self):
		return self.get_value() == 21

	def display(self, show_dealer_cards=False):
		sleep(.5)
		print(f'''{"Dealer's" if self.dealer else "Your"} hand:''')

		for i, card in enumerate(self.cards):
			if i == 0 and self.dealer and not self.is_blackjack() and not show_dealer_cards:
				print("- [HIDDEN]")
			else:
				print(f"- {card}")

		if not self.dealer:
			print(f"Value: {self.get_value()}")

		print()


class Game:

	def play(self):
		print("\nWelcome to the \"Terminal Blackjack\"!")
		game_number = 0
		games_to_play = None

		while not games_to_play:
			try:
				games_to_play = int(input("How many games do you want to play?: "))
			except:
				print("Please, enter a valid number.")

		while game_number < games_to_play:
			if game_number > 0: input("Press Enter to continue... ")
			print()
			game_number += 1
			deck = Deck()
			deck.shuffle()
			player_hand = Hand()
			dealer_hand = Hand(dealer=True)

			for _ in range(2):
				player_hand.add_card(deck.deal(1))
				dealer_hand.add_card(deck.deal(1))

			print("=" * 30)
			print(f"Game {game_number} of {games_to_play}")
			print("=" * 30)
			print()

			player_hand.display()
			dealer_hand.display()

			if self.check_winner(player_hand, dealer_hand):
				continue

			choice = None

			while player_hand.get_value() < 21 and choice not in ["stand", "s"]:
				sleep(.5)
				choice = input("\"Hit\" or \"Stand\"?: ").lower()

				while choice not in ["hit", "h", "stand", "s"]:  # validate choice input
					choice = input("Please, enter \"Hit\" or \"Stand\" (\"H\" or \"S\"): ").lower()

				print()

				if choice in ["hit", "h"]:
					player_hand.add_card(deck.deal(1))
					player_hand.display()

			if self.check_winner(player_hand, dealer_hand):
				continue

			while dealer_hand.get_value() < 17:
				dealer_hand.add_card(deck.deal(1))

			dealer_hand.display(show_dealer_cards=True)

			if self.check_winner(player_hand, dealer_hand):
				continue

			sleep(.5)
			print("Reveal:", f"Your hand: {player_hand.get_value()}", f"Dealer's hand: {dealer_hand.get_value()}\n", sep="\n")
			self.check_winner(player_hand, dealer_hand, game_over=True)

		sleep(1)
		print("Thanks for playing!\n")

	def check_winner(self, player_hand, dealer_hand, game_over=False):
		if not game_over:
			if player_hand.get_value() > 21:
				sleep(.5)
				print("You busted. Dealer wins.\n")
				return True
			elif dealer_hand.get_value() > 21:
				sleep(.5)
				print("Dealer busted. You win.\n")
				return True
			elif player_hand.is_blackjack() and dealer_hand.is_blackjack():
				sleep(.5)
				print("Both players have blackjack! Tie.\n")
				return True
			elif player_hand.is_blackjack():
				sleep(.5)
				print("Blackjack! You win.\n")
				return True
			elif dealer_hand.is_blackjack():
				sleep(.5)
				print("Blackjack! Dealer wins.\n")
				return True
		else:
			if player_hand.get_value() > dealer_hand.get_value():
				sleep(.5)
				print("You win.\n")
			elif player_hand.get_value() == dealer_hand.get_value():
				sleep(.5)
				print("Tie.\n")
			else:
				sleep(.5)
				print("Dealer wins.\n")

			return True

		return False


if __name__ == "__main__":
	game = Game()
	game.play()
