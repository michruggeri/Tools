#!/usr/bin/env python3


"""
This script is a simple game of baba-nuki/old maid/pouilleux/etc,
played with the computer as the opponent.
"""


import random

"""
Defining the basic card elements as tuples 
"""
suits = ("Hearts", "Diamonds", "Clubs", "Spades")
values = ("7","8","9","10","Jack","Queen","King","Ace")
jokers = ("Joker",)


def samecolor(a:str,b:str) -> bool:
  """
  Checks if two seeds are different, and of the same color.
  """
  if {a,b} == {"Hearts","Diamonds"} or {a,b} == {"Clubs","Spades"}:
    return True
  else:
    return False


class Card:
  """
  Class representing a card, with suit and value
  """
  def __init__(self,suit:str,value:str) -> None:
    self.suit  = suit
    self.value = value

  def __str__(self) -> str:
    if self.value == "Joker" :
      return f"{self.value}!"
    else:
      return f"{self.value} of {self.suit}"


class Pile:
  """
  Class defining a pile of cards
  """
  def __init__(self) -> None:
    self.cards=[]
    self.ncards = len(self.cards)

  def __str__(self) -> str:
    return f"Pile of {self.ncards} cards"

  def printcards(self) -> None:
    print(self)
    for i in self.cards:
      print(i)

  def shuffle(self) -> None:
    print("Shuffling...")
    random.shuffle(self.cards)

  def add(self,card:Card) -> None:
    self.cards.append(card)
    self.ncards = len(self.cards)

  def discard(self,card:Card) -> None:
    self.cards.remove(card)
    self.ncards = len(self.cards)

  def remove_pairs(self) -> None:
    to_rem = set() 
    for i in self.cards:
      for j in self.cards:
        if samecolor(i.suit,j.suit) and i.value==j.value:
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
        c = Card(i,j)
        self.cards.append(c)
    for i in jokers:
        c = Card("X",i)
        self.cards.append(c)
    self.ncards = len(self.cards)

  def deal(self) -> (Pile,Pile):
    self.shuffle()
    hand1 = Pile()
    hand2 = Pile()
    for i in range(self.ncards):
      if i%2 == 0:
        hand1.add(self.cards[i])
      else:
        hand2.add(self.cards[i])
    return hand1,hand2


def main() -> None:
  """
  Main function: the actual game
  """
  a = Deck()

  print("Game start!")
  h1,h2=a.deal()
  h1.remove_pairs()
  h2.remove_pairs()

  if(h1.ncards < h2.ncards):
    play = "P1"
  else:
    play="P2"

  while h1.ncards > 0 and h2.ncards > 0:
    print("P1:")
    h1.printcards()
    print()
    print("P2:")
    print(h2)
    chosen = input()
    if play == "P1":
      chosen = ""
      choices = []
      for i in range(h2.ncards):
        choices.append(str(i+1))
      while chosen not in choices:
        chosen =(input(f"Choose a card to pick (between 1 and {h2.ncards}): "))
      chosen = int(chosen)
      card = h2.cards[chosen-1]
      print(f"You chose the {card}")
      h1.add(card)
      h2.discard(card)
      h1.remove_pairs()
      play = "P2"
    else:
      chosen = input(f"The opponent is choosing!")
      card = random.choice(h1.cards)
      print(f"The opponent chose the {card}")
      h1.discard(card)
      h2.add(card)
      h2.remove_pairs()
      play = "P1"
    print()
  if h1.ncards == 0:
    print("You won!")
  else:
    print("You lose!")
  print("P1:")
  h1.printcards()
  print()
  print("P2:")
  h2.printcards()


if __name__ == "__main__":
    main()
