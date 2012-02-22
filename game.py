import copy

from player import *
from cards import *

class Game(object):
    """
    Abstract class
    """
    deck = None     #abstractable? Ex. Yomi, multi-deck
    players = []
    pile_groups = {}
    phases = []
    def __init__(self, deck):
        self.deck = deck
        self.pile_groups['init'] = PileGroup({
            #Shallow copy of list, keeps references to same cards
            'init': Pile(cards=copy.copy(deck.cards))
        })

    def run(self):
        if not self.phases:
            return
        phase = self.phases[0]
        while phase:
            phase.enter()
            phase.execute()
            phase.exit()
            phase = phase.next_phase

class Phase(object):
    """
    This class manages Game logic.
    Ex. DrawPhase, DealPhase, PlayPhase, EndTurnPhase

    A Phase performs some action on the Game, possibly requiring input.
    A Phase leads into another Phase, as managed by the Game.

    Phases may encompass multiple SubPhases.
    Ex. TrickPhase of 4 PlayPhases
    Ex. InterruptPhase (i.e. in Mahjong, Asshole)
    """
    next_phase = None
    def __init__(self, next_phase):
        self.next_phase = next_phase

    def enter(self):
        '''
        Allow for InterruptPhases, etc.
        '''
        pass

    def execute(self):
        '''
        Main function of Phase.
        '''
        pass

    def exit(self):
        '''
        Cleanup.
        '''
        pass
        
class DealPhase(Phase):
    """
    Deals from a main Pile to several other Piles.
    """
    def __init__(self, main_pile, receiving_piles, shuffle_first=True, next_phase=None):
        Phase.__init__(self, next_phase)
        self.main_pile = main_pile
        self.receiving_piles = receiving_piles
        self.shuffle_first = shuffle_first

    def enter(self):
        if (self.shuffle_first):
            self.main_pile.shuffle()

    def execute(self):
        index = 0
        while self.main_pile.cards:
            self.receiving_piles[index].draw_from(self.main_pile)
            index = (index + 1) % len(self.receiving_piles)

class PileGroup(object):
    """
    This class aggregates Piles of various sorts
    Ex. A TrickGame has one PileArea per player, each with a TrickPile and HandPile
    Ex. Any game generally has a GeneralPileArea for a DrawPile, DiscardPile, etc.
    """
    piles = {}
    def __init__(self, piles):
        self.piles = piles
        pass
        
        
class Big2(Game):
    def __init__(self, players=[Player() for x in range(4)]):
        this.deck = Deck()
        this.players = players
        this.player_hands = {}
        for p in this.players:
            this.player_hands[p] = Pile()


