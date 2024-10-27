import random
from random import shuffle
import pdb
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
bet_placed = 0
playing = False
player_turn = False
dealer_turn = False
player_hit = True
dealer_hit = True

class Card:
    """
    A class representing a playing card.

    Attributes
    ----------
    suit : str
        The suit of the card (e.g., Hearts, Diamonds, Spades, Clubs).
    rank : str
        The rank of the card (e.g., Two, Three, Four, ..., Jack, Queen, King, Ace).
    value : int
        The numerical value of the card, based on the standard Blackjack rules.

    Methods
    -------
    __init__(self, suit, rank)
        Initializes the card with the given suit and rank.

    __str__(self)
        Returns a string representation of the card in the format "Rank of Suit".
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    """
    A class representing a deck of playing cards.

    Attributes
    ----------
    all : list
        A list of Card objects representing all the cards in the deck.

    Methods
    -------
    __init__(self)
        Initializes the deck with 52 cards, one of each suit and rank combination.

    shuffle(self)
        Shuffles the order of the cards in the deck.

    deal(self)
        Removes and returns the top card from the deck.
    """
    def __init__(self):
        self.all = []
        for suit in suits:
            for rank in ranks:
                self.all.append(Card(suit, rank))

    def shuffle(self):
        """
        Shuffles the order of the cards in the deck.
        """
        random.shuffle(self.all)

    def deal(self):
        """
        Removes and returns the top card from the deck.

        Returns
        -------
        Card
            The top card from the deck.
        """
        return self.all.pop()

class Hand():
    """
    A class representing a hand of playing cards in a game.

    Attributes
    ----------
    cards : list
        A list of Card objects representing the cards in the hand.
    values : dict
        A dictionary mapping card ranks to their numerical values in Blackjack.
    aces : int
        The number of aces in the hand.
    total_value : int
        The total value of the hand, considering aces as either 1 or 11.

    Methods
    -------
    add_card(card)
        Adds a card to the hand.

    ace_choice()
        Handles the case where an ace is added to the hand. Prompts the user to choose a value for the ace (1 or 11).

    find_value(card)
        Calculates the total value of the hand after adding a new card.

    __str__()
        Returns a string representation of the hand, listing the cards in the hand.
    """
    def __init__(self):
        self.cards = []
        self.values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
        self.aces = 0
        self.total_value = 0

    def add_card(self, card):
        self.cards.append(card)

    def ace_choice(self):
        print('Looks like an ace!!!')
        while True:
            try:
                choice = int(input('Enter value for ace (1 or 11): '))
                if choice in [1, 11]:
                    break
                else:
                    print("Please enter either 1 or 11.")
            except ValueError:
                print("Looks like you did not enter an integer!")

        self.values['Ace'] = choice


    def find_value(self, card):
        self.total_value = self.total_value + self.values[card.rank]
        print(self.total_value)
        return self.total_value


    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

class Chips():
    def __init__(self):
        self.balance = 100

    def add(self, amount):
        self.balance = self.balance + amount
        return self.balance
    def subtract(self, amount):
        self.balance = self.balance - amount
        return self.balance

def place_bet():
    global amount
    try:
        amount = int(input('Enter betting amount'))
    except:
        print("Looks like you did not enter an integer!")
        amount = int(input('Enter betting amount'))

    while amount > chips.balance:
        print('Insufficient funds. Please try with less')
        amount = int(input('Enter betting amount'))
    return amount

def hit_or_stand(deck, hand):
    global player_hit
    player_hit = True
    reply = input('Do you want to hit? (Yes or No): ').capitalize()

    while reply != 'Yes' and reply != 'No':
        print('Invalid input')
        reply = input('Do you want to hit? (Yes or No): ').capitalize()
    if reply == 'Yes':
        hit(deck, hand)
    else:
        player_hit = False
        return player_hit

def hit(deck, hand):
    """
    This function deals a new card to the player's hand and updates the hand's total value.
    If the dealt card is an Ace, it prompts the player to choose a value for the Ace (1 or 11).

    Parameters:
    deck (Deck): The deck from which the card is dealt.
    hand (Hand): The player's hand to which the card is added.

    Returns:
    None
    """
    card = deck.deal()
    if card.rank == 'Ace':
        hand.ace_choice()
        hand.add_card(card)
    else:
        hand.add_card(card)

def show_some(player, dealer):
    print(player)
    print(dealer.cards[0])

def show_all(player, dealer):
    print(player)
    print(dealer)

def player_busts(values, bet_placed):
    print(f'Players hand has exceeded 21. Value of cards is {values}')
    chips.subtract(bet_placed)
    print(f'Current balance is now {chips.balance}')

def dealer_wins(values_dealer, values_player, bet_placed):
    print(f"Dealer beat player. Dealer's value of cards was {values_dealer}, while player's value of cards was {values_player} ")
    chips.subtract(bet_placed)
    print(f'Current balance is now {chips.balance}')

def dealer_busts(bet_placed):
    print('Dealer has busted. Player wins')
    chips.add(bet_placed*2)
    print(f'Current balance is now {chips.balance}')

def player_wins(bet_placed):
    print("Dealer's hand has exceeded 17 but not higher than player. Player wins")
    chips.add(bet_placed * 2)
    print(f'Current balance is now {chips.balance}')

def push():
    print('Values of hands are equal. Push')
    print(f'Current balance is now {chips.balance}')

while True:
    # Initialize player's chips
    chips = Chips()

    # Create a new deck of cards and shuffle it
    deck = Deck()
    deck.shuffle()

    # Create player and dealer hands
    hand_player = Hand()
    hand_dealer = Hand()

    # Place a bet
    place_bet()

    # Deal initial two cards to player and dealer
    for i in range(2):
        card = deck.deal()
        if card.rank == 'Ace':
            # If the card is an Ace, prompt the player to choose its value
            hand_player.ace_choice()
            hand_player.add_card(card)
            hand_player.find_value(card)
            hand_dealer.add_card(deck.deal())
            hand_dealer.find_value(hand_dealer.cards[-1])
        else:
            # Add the card to the player's hand and update its value
            hand_player.add_card(card)
            hand_player.find_value(card)
            hand_dealer.add_card(deck.deal())
            hand_dealer.find_value(hand_dealer.cards[-1])

    # Show the player's hand and the dealer's first card
    show_some(hand_player, hand_dealer)

    # Player's turn to hit or stand
    while player_hit == True:
        if player_hit == False:
            break
        # Prompt the player to hit or stand
        hit_or_stand(deck, hand_player)
        # Show the player's hand and the dealer's first card
        show_some(hand_player, hand_dealer)
        # Calculate the value of the player's last card
        card_value = hand_player.find_value(hand_player.cards[-1])
        if card_value > 21:
            # If the player's hand exceeds 21, they bust
            player_busts(hand_player.total_value, amount)
            # Show the final hands
            show_all(hand_player, hand_dealer)
            # End the dealer's turn
            dealer_hit = False
            break

    # If the player's hand does not exceed 21, the dealer's turn begins
    if hand_player.total_value <= 21:
        while dealer_hit == True:
            if hand_dealer.total_value > 17:
                break
            # Dealer hits until their hand value is greater than 17
            hit(deck, hand_dealer)
            # Show the final hands
            show_all(hand_player, hand_dealer)

        # Check the outcome of the game
        if hand_dealer.total_value > 21:
            # If the dealer's hand exceeds 21, they bust
            dealer_busts(amount)
            show_all(hand_player, hand_dealer)
        elif hand_dealer.total_value > hand_player.total_value:
            # If the dealer's hand is higher than the player's, the dealer wins
            dealer_wins(hand_dealer.total_value, hand_player.total_value, amount)
            show_all(hand_player, hand_dealer)
        elif hand_player.total_value > hand_dealer.total_value and hand_player.total_value <= 21:
            # If the player's hand is higher than the dealer's, the player wins
            player_wins(amount)
            show_all(hand_player, hand_dealer)
        else:
            # If the player's and dealer's hands have the same value, it's a push
            push()
            show_all(hand_player, hand_dealer)






