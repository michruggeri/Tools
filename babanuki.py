#!/usr/bin/env python3


"""
This script is a simple game of baba-nuki/old maid/pouilleux/etc,
played with the computer as the opponent.
"""


import random
from typing import Tuple

suits = ("Hearts", "Diamonds", "Clubs", "Spades")
values = ("7", "8", "9", "10", "Jack", "Queen", "King", "Ace")
jokers = ("Joker",)


def samecolor(seed_a: str, seed_b: str) -> bool:
    """
  Checks if two seeds are different, and of the same color.
  """
    return {seed_a, seed_b} == {"Hearts", "Diamonds"} or {seed_a, seed_b} == {
        "Clubs",
        "Spades",
    }


class Card:
    """
    Class representing a card, with suit and value
    """

    def __init__(self, suit: str, value: str) -> None:
        self.suit = suit
        self.value = value

    def __str__(self) -> str:
        if self.value == "Joker":
            return f"{self.value}!"
        return f"{self.value} of {self.suit}"


class Pile:
    """
    Class defining a pile of cards
    """

    def __init__(self) -> None:
        self.cards = []
        self.ncards = len(self.cards)

    def __str__(self) -> str:
        return f"Pile of {self.ncards} cards"

    def printcards(self) -> None:
        """
        Prints the pile and the cards it contains
        """
        print(self)
        for i in self.cards:
            print(i)

    def shuffle(self) -> None:
        """
        Shuffles the deck
        """
        print("Shuffling...")
        random.shuffle(self.cards)

    def add(self, card: Card) -> None:
        """
        Adds a card to the pile
        """
        self.cards.append(card)
        self.ncards = len(self.cards)
        random.shuffle(self.cards)

    def discard(self, card: Card) -> None:
        """
        Removes a card from the pile
        """
        self.cards.remove(card)
        self.ncards = len(self.cards)
        random.shuffle(self.cards)

    def remove_pairs(self) -> None:
        """
        Removes from the hand all cards with the same values and colors
        """
        to_rem = set()
        for i in self.cards:
            for j in self.cards:
                if samecolor(i.suit, j.suit) and i.value == j.value:
                    to_rem.add(i)
        for i in to_rem:
            self.discard(i)


class Deck(Pile):
    """
    Class defining a deck of cards
    """

    def __init__(self) -> None:
        self.cards = []
        for i in suits:
            for j in values:
                card = Card(i, j)
                self.cards.append(card)
        for i in jokers:
            card = Card("X", i)
            self.cards.append(card)
        self.ncards = len(self.cards)

    def deal(self) -> Tuple[Pile, Pile]:
        """
        Shuffles the deck and deals two hands, till the deck is empty
        """
        self.shuffle()
        hand1 = Pile()
        hand2 = Pile()
        for i in range(self.ncards):
            if i % 2 == 0:
                hand1.add(self.cards[i])
            else:
                hand2.add(self.cards[i])
        return hand1, hand2


def main() -> None:
    """
    Main function: the actual game
    """
    deck = Deck()

    print("Game start!")
    hand_1, hand_2 = deck.deal()
    hand_1.remove_pairs()
    hand_2.remove_pairs()

    if hand_1.ncards < hand_2.ncards:
        play = "P1"
    else:
        play = "P2"

    while hand_1.ncards > 0 and hand_2.ncards > 0:
        print("P1:")
        hand_1.printcards()
        print()
        print("P2:")
        print(hand_2)
        chosen = input()
        if play == "P1":
            chosen = ""
            choices = []
            for i in range(hand_2.ncards):
                choices.append(str(i + 1))
            while chosen not in choices:
                chosen = input(
                    f"Choose a card to pick (between 1 and {hand_2.ncards}): "
                )
            chosen = int(chosen)
            card = hand_2.cards[chosen - 1]
            print(f"You chose the {card}")
            hand_1.add(card)
            hand_2.discard(card)
            hand_1.remove_pairs()
            play = "P2"
        else:
            chosen = input("The opponent is choosing!")
            card = random.choice(hand_1.cards)
            print(f"The opponent chose the {card}")
            hand_1.discard(card)
            hand_2.add(card)
            hand_2.remove_pairs()
            play = "P1"
        print()
    if hand_1.ncards == 0:
        print("You won!")
    else:
        print("You lose!")
    print("P1:")
    hand_1.printcards()
    print()
    print("P2:")
    hand_2.printcards()


if __name__ == "__main__":
    main()
