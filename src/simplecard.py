from cardvalue import CardValue


class SimpleCard:

    def __init__(self, value, suit):
        """Initializes a SimpleCard object.

        Args:
            value (int): The card's value
            suit (str): The card's suit
        """
        self.value = value
        self.suit = suit
