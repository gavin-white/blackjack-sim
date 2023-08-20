import random
from cardsuit import CardSuit
from cardvalue import CardValue
from simplecard import SimpleCard

from simplifiedshoe import SimplifiedShoe


class Shoe:
    """Represents an object that can be used to simulate a blackjack shoe."""

    def __init__(self, num_decks, penetration, counts={2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0, 8: 0, 9: 0, 10: -1, 1: -1}):
        """Initializes a Shoe object which can be used to simulate a blackjack shoe. The shoe is represented as a list
        of integers, where each integer represents a card. The cards are represented as follows:
        1 = Ace
        2-9 = 2-9
        10 = 10, Jack, Queen, King

        Args:
            num_decks (Int): The number of decks in the shoe
            penetration (Float): The penetration of the shoe, represented as a decimal between 0 and 1. For example, a
            penetration of 0.75 means that the shoe will be reshuffled when there are 75% of the cards have been dealt.
            counts (dict, optional): What count value each card has.
        """
        self._shoe = SimplifiedShoe(num_decks, penetration, counts)
        self._num_decks = num_decks
        self._shuffle()

    def _enhance(self, card):
        """Enhances a given integer card value to a SimpleCard object, providing it with suit and face value
        consistent with what has been dealt so far.

        Args:
            card (Int): The card to enhance in integer form
        """
        if card == 1:
            return SimpleCard(CardValue.ACE, self._suit_pools[CardValue.ACE].pop())
        elif card == 10:
            ten_card = self._ten_pool.pop()
            return SimpleCard(ten_card, self._suit_pools[ten_card].pop())
        else:
            return SimpleCard(card, self._suit_pools[card].pop())

    def _shuffle(self):
        """Shuffles the shoe.
        """
        self._ten_pool = [CardValue.TEN, CardValue.JACK, CardValue.QUEEN, CardValue.KING] * 4 * self._num_decks
        self._suit_pools = {value: [CardSuit.CLUBS, CardSuit.DIAMONDS, CardSuit.HEARTS, CardSuit.SPADES] * self._num_decks for value in CardValue}
        random.shuffle(self._ten_pool)
        for pool in self._suit_pools.values():
            random.shuffle(pool)


    def draw(self):
        """Draws a card from the shoe and updates the count.

        Returns:
            Int: The card that was drawn
        """
        return self._enhance(self._shoe.draw())
    
    def draw_face_down(self):
        """Draws a card from the shoe without updating the count. Once the card is revealed, the card_revealed method
        should be called to update the count.

        Returns:
            Int: The card that was drawn.
        """
        return self._enhance(self._shoe.draw_face_down())
    
    def card_revealed(self, card):
        """Updates the count based on the card that was revealed. This is necessary to account for cards that are
        dealt face down, and then revealed later. Thus, the count will only be updated when the card is revealed.

        Args:
            card (SimpleCard): The card that was revealed
        """
        self._shoe.card_revealed(card.int_value())

    def get_count(self):
        """Returns the running count of the shoe.

        Returns:
            Int: The running count of the shoe
        """
        return self._shoe.get_count()
    
    def get_true_count(self):
        """Returns the true count of the shoe, which is calculated by dividing the running count by the number of
        decks remaining in the shoe.

        Returns:
            Int: The true count of the shoe
        """
        return self._shoe.get_true_count()
    
    def start_hand(self):
        """Called at the beginning of a new hand. If the cut card has been dealt, the shoe will be shuffled
        and the count will be reset to 0.

        Returns:
            Boolean: True if the shoe was shuffled, False otherwise
        """
        shuffled = self._shoe.start_hand()
        if shuffled:
            self._shuffle()
        return shuffled