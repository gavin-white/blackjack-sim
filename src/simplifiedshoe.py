import random


class SimplifiedShoe:
    """Represents an object that can be used to simulate a blackjack shoe. The cards have a simplified representation
    of simply an integer value corresponding to their value in the game of blackjack. There are no suits or face cards.
    """

    def __init__(self, num_decks, penetration, counts={2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0, 8: 0, 9: 0, 10: -1, 1: -1}):
        """Initializes a Shoe object which can be used to simulate a blackjack shoe. The shoe is represented as a list
        of integers, where each integer represents a card. The cards are represented as follows:
        1 = Ace
        2-9 = 2-9
        10 = 10, Jack, Queen, King
        Provides operations to draw a card from the shoe, automatically shuffles and tracks the count, and provides methods to
        retrieve the running count and true count.

        Args:
            num_decks (Int): The number of decks in the shoe
            penetration (Float): The penetration of the shoe, represented as a decimal between 0 and 1. For example, a
            penetration of 0.75 means that the shoe will be reshuffled when there are 75% of the cards have been dealt.
            counts (dict, optional): . Defaults to {2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0, 8: 0, 9: 0, 10: -1, 1: -1}.
        """
        self.cards = self._get_decks(num_decks)
        self.counts = counts
        self._index = 0
        self._count = 0
        self._cut_card = len(self.cards) * penetration

    def draw(self):
        """Draws a card from the shoe and updates the count.

        Returns:
            Int: The card that was drawn
        """
        card = self.draw_face_down()
        self._count += self.counts[card]
        return card
    
    def draw_face_down(self):
        """Draws a card from the shoe without updating the count. Once the card is revealed, the card_revealed method
        should be called to update the count.

        Returns:
            Int: The card that was drawn.
        """
        self._index += 1
        return self.cards[self._index - 1]
    
    def card_revealed(self, card):
        """Updates the count based on the card that was revealed. This is necessary to account for cards that are
        dealt face down, and then revealed later. Thus, the count will only be updated when the card is revealed.

        Args:
            card (Int): The card that was revealed
        """
        self._count += self.counts[card]

    def get_count(self):
        """Returns the running count of the shoe.

        Returns:
            Int: The running count of the shoe
        """
        return self._count
    
    def get_true_count(self):
        """Returns the true count of the shoe, which is calculated by dividing the running count by the number of
        decks remaining in the shoe.

        Returns:
            Int: The true count of the shoe
        """
        return int(self._count / ((len(self.cards) - self._index) / 52))
    
    def _shuffle(self):
        """Shuffles the shoe, resetting the index and count to 0.
        """
        random.shuffle(self.cards)
        self._index = 0
        self._count = 0
    
    def start_hand(self):
        """Called at the beginning of a new hand. If the cut card has been dealt, the shoe will be shuffled
        and the count will be reset to 0.

        Returns:
            Boolean: True if the shoe was shuffled, False otherwise
        """
        if self._index > self._cut_card:
            self._shuffle()
            return True
        return False

    def _get_decks(self, num_decks):
        """Returns a list of cards representing the number of decks specified.

        Args:
            num_decks (Int): The number of decks to include in the shoe

        Returns:
            List[Int]: A list of cards representing the number of decks specified
        """
        single_suit = []
        for num in range(1,11):
            single_suit.append(num)
        for i in range(0,3):
            single_suit.append(10)

        deck = []
        for i in range(0, num_decks * 4):
            deck.extend(single_suit)

        random.shuffle(deck)
        return deck