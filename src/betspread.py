class BetSpread:
    """Represents an object that can be used to retrieve bet values based on the true count.
    """

    def __init__(self, bet_spread):
        """Initializes a BetSpread object which can be used to quickly access what the bet should be for a given
        true count based on a defined spread. The given spread takes the form of a dictionary where the keys are
        true count values and the values are the corresponding bets. Any gaps between true counts will be filled
        with the next lowest bet. Any true count above the defined spread's maximum true count will take the bet
        value of the highest true count in the defined spread, and vice versa for true counts below the defined
        spread's minimum.

        Args:
            bet_spread (dict(int: int)): A dictionary containing the betting values for particular true counts.
        """
        self._spread = {}
        spread_max_count = max(bet_spread.keys())
        spread_min_count = min(bet_spread.keys())
        self._pivot = spread_max_count
        self._low_bet = bet_spread[spread_min_count]
        self._high_bet = bet_spread[spread_max_count]
        prev_bet = self._low_bet
        for tc in range(spread_min_count, spread_max_count + 1):
            if tc in bet_spread:
                self._spread[tc] = bet_spread[tc]
                prev_bet = bet_spread[tc]
            else:
                self._spread[tc] = prev_bet

    
    def get_bet(self, true_count):
        """Retrieves the correct bet for this spread based on the given true count.

        Args:
            true_count (int): the true count

        Returns:
            int: the bet
        """
        if true_count in self._spread:
            return self._spread[true_count]
        elif true_count > self._pivot:
            return self._high_bet
        else:
            return self._low_bet