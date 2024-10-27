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
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    def __init__(self):
        self.all = []
        for suit in suits:
            for rank in ranks:
                self.all.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.all)

    def deal(self):
        return self.all.pop()

class Hand():
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
    chips = Chips()
    deck = Deck()
    deck.shuffle()
    hand_player = Hand()
    hand_dealer = Hand()
    place_bet()

    for i in range(2):
        card = deck.deal()
        if card.rank == 'Ace':
            hand_player.ace_choice()
            hand_player.add_card(card)
            hand_player.find_value(card)
            hand_dealer.add_card(deck.deal())
            hand_dealer.find_value(hand_dealer.cards[-1])
        else:
            hand_player.add_card(card)
            hand_player.find_value(card)
            hand_dealer.add_card(deck.deal())
            hand_dealer.find_value(hand_dealer.cards[-1])

    show_some(hand_player, hand_dealer)

    while player_hit == True:
        if player_hit == False:
            break
        hit_or_stand(deck, hand_player)
        show_some(hand_player, hand_dealer)
        card_value = hand_player.find_value(hand_player.cards[-1])
        if card_value > 21:
            player_busts(hand_player.total_value, amount)
            show_all(hand_player, hand_dealer)
            dealer_hit = False
            break

    if hand_player.total_value <= 21:

       while dealer_hit == True:
           if hand_dealer.total_value > 17:
               break
           hit(deck, hand_dealer)
           #current_value = hand_dealer.find_value(hand_dealer.cards[-1])
           show_all(hand_player, hand_dealer)


       if hand_dealer.total_value > 21:
           dealer_busts(amount)
           show_all(hand_player, hand_dealer)
           break
       elif hand_dealer.total_value > hand_player.total_value:
           dealer_wins(hand_dealer.total_value, hand_player.total_value, amount)
           show_all(hand_player, hand_dealer)
           break
       elif hand_player.total_value > hand_dealer.total_value and hand_player.total_value <= 21 :
           player_wins(amount)
           show_all(hand_player, hand_dealer)
           break
       else:
           push()
           show_all(hand_player, hand_dealer)
           break














