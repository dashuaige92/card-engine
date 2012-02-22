import copy
import random

class Card(object):
    """
    A Card represents a single card of a playing card deck
    The card type is defined by generalizable attributes
    It can store any card states independent of game state

    A Card should be part of a Deck
    """

    attr = {}
    deck = None
    def __init__(self, attr, deck=None):
        self.attr = attr
        self.deck = deck

    def __str__(self):
        return attr.__str__()

class PokerCard(Card):
    """
    Comparisons and value assignments can be abstracted.
    Ex. Blackjack, Trump Suit, Big2

    Jokers represented by 'joker' suit
    'number' = 1 for little Joker, 2 for big Joker
    """
    def __init__(self, suit, number, deck=None):
        Card.__init__(self, {
            'suit': suit,
            'number': number,
        }, deck)

    def __str__(self):
        if self.attr['suit'] == 'joker':
            return ('Big' if 2 else 'Little') + ' ' + self.attr['suit']
        face_cards = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
        return str(face_cards.get(self.attr['number'], self.attr['number'])) + ' of ' + self.attr['suit']
        
class Deck(object):
    """
    A Deck aggregates a set of Cards
    It aggregates Piles and manages distribution of Cards among them

    Ex. default 52 card Deck, 54 card Deck
    Ex. Euchre Deck, Tractor Deck
    Ex. Sanguosha Deck, Yomi Deck

    Deck also provides an ordering on the Cards if necessary
    """

    cards = []
    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        return self.cards.__str__()

class PokerDeck(Deck):
    """
    A Deck aggregates a set of Cards
    It aggregates Piles and manages distribution of Cards among them

    Ex. default 52 card Deck, 54 card Deck
    Ex. Euchre Deck, Tractor Deck
    Ex. Sanguosha Deck, Yomi Deck
    """
    def __init__(self, cards=None, preset=True, jokers=False, number_range=range(1, 14), num_decks=1):
        if preset:
            cards = [PokerCard(suit=x, number=y, deck=self) for y in number_range for x in ['spades', 'hearts', 'diamonds', 'clubs']]
            if jokers:
                cards += [PokerCard(suit='joker', number=1, deck=self), PokerCard(suit='joker', number=2, deck=self)]
            cards *= num_decks
        #preset False -> cards explicitly defined and stored
        self.cards = cards
        Deck.__init__(self, cards)

class Pile(object):
    """
    Piles aggregate cards from a Deck into smaller components
    used for game logic
    Ex. HandPile, DrawPile, DiscardPile, TrashPile
    Ex. SlotPile

    This class provides an ordering, i.e. "top" and "bottom" of the Pile
    """

    '''
    players designates certain players to roles
    Roles allow for game logic, i.e. Pile visibility and play_card_from
    '''
    def __init__(self, cards, players=copy.copy({})):
        self.cards = cards
        self.players = players
        
    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        self.cards.sort()

    '''
    Take cards from a pile and returns them
    Must be transferred to another pile
    '''
    def take_cards(self, method='draw', count=1, assert_func=None):
        '''
        Returns the top N cards, or remaining M<N cards, while removing them.
        '''
        if (method == 'draw'):
            a = [self.cards.pop() for x in range(min(len(self.cards), count))]
            return a

        
    def draw_from(self, pile):
        if not pile.cards:
            print("EmptyPile")
            #raise EmptyPileError
        else:
            card = pile.take_cards()
            self.cards += card

    def __str__(self):
        return '[' + ', '.join([str(x) for x in self.cards]) + ']'

    def __repr__(self):
        return 'Pile(cards=%r)' % id(self.cards) + ' at %r' % id(self)

class SuperPile(object):
    """
    Allows for clumping of several cards for certain use cases
    Ex. SuperPile of poker hands in Big2
    Ex. SuperPile of TrickPiles owned by each player
    """
    def __init__(self):
        pass
