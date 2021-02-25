import unittest 
from card_suite import Card

class TestCard(unittest.TestCase):
    """Tests for the class Card"""
    
    def setUp(self):
        """
        Create a few Cards to use in the test methods
        """
        self.card1 = Card('3', 'Diamond')
        self.card2 = Card('5', 'Spade')
        self.card3 = Card('10', 'Club')

    def test_print_card(self):
        """Test that a card can print itself properly"""
        printed_card = "3 of Diamond's"
        card_printed = self.card1.ReturnCard()
        self.assertEqual(printed_card, card_printed)

    def test_card_rank(self):
        """Test that a card's rank attribute is set properly"""
        card_rank = '10'
        self.assertEqual(card_rank, self.card3.rank)

if __name__== '__main__':
    unittest.main()
