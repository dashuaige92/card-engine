"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest
from cards import *
from game import *
from player import *
from logic import *

class SetupTest(unittest.TestCase):
    class TestGame(Game):
        """
        Sets up basic players to allow testing for Deck implementation.
        Ex. Dealing, Resetting
        """
        def __init__(self, deck=PokerDeck()):
            Game.__init__(self, deck)
            self.deck = deck
            self.players = [Player() for x in range(4)]
            self.pile_groups['player'] = {}
            for p in self.players:
                self.pile_groups[p] = PileGroup({
                    'hand': Pile([])
                })
            self.phases = [DealPhase(
                main_pile=self.pile_groups['init'].piles['init'],
                receiving_piles=[self.pile_groups[p].piles['hand'] for p in self.players])]
        
    def setUp(self):
        '''
        Starts game, game deals hands
        '''
        self.game = self.TestGame()

    def test_deal(self):
        self.assertEqual(len(self.game.pile_groups['init'].piles['init'].cards), 52)
        self.game.run()
        self.assertIsInstance(self.game.pile_groups, dict)
        self.assertEqual(len(self.game.pile_groups['init'].piles['init'].cards), 0)
        for p in self.game.players:
            self.assertEqual(len(self.game.pile_groups[p].piles['hand'].cards), 13)
            print(self.game.pile_groups[p].piles['hand'])
            print(repr(self.game.pile_groups[p].piles['hand']))

if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(SetupTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
