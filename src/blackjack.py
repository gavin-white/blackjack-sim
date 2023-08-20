from betspread import BetSpread
from defaultstrategy import strategy as strategy_table
from simplifiedshoe import SimplifiedShoe

class BlackJackSimulator:
    """
    Represents a blackjack simulator.
    """

    def __init__(self, num_decks, penetration, bet_spread, strategy_table, bankroll=0):
        self._bet_spread = BetSpread(bet_spread)
        self._strategy_table = strategy_table
        self._shoe = SimplifiedShoe(num_decks, penetration)
        self._player_cash = bankroll
        self._player_spending = 0

    def play_hand(self):
        self._shoe.start_hand()
        player_bet = self._bet_spread.get_bet(self._shoe.get_true_count())
        self._deal()

        dealer_total = self._calculate_total(self._dealer_hand)
        player_total = self._calculate_total(self._player_hand)

        if dealer_total == 21 and player_total == 21:
            # blackjack push
            self._player_spending += player_bet
            self._shoe.card_revealed(self._dealer_hand[1])
            return 0
        elif dealer_total == 21 and player_total != 21:
            # dealer blackjack
            self._player_spending += player_bet
            self._player_cash -= player_bet
            self._shoe.card_revealed(self._dealer_hand[1])
            return -player_bet
        elif player_total == 21:
            # blackjack
            self._player_spending += player_bet
            self._player_cash += 1.5 * player_bet
            self._shoe.card_revealed(self._dealer_hand[1])
            return 1.5 * player_bet

        player_outcomes = self._play_player_hand(self._dealer_hand[0], self._player_hand, self._shoe)
        dealer_outcome = self._play_dealer_hand(self._dealer_hand, self._shoe)
        dealer_outcome = dealer_outcome if dealer_outcome <= 21 else 0
        self._shoe.card_revealed(self._dealer_hand[1])

        sum = 0
        for outcome in player_outcomes:
            self._player_spending += player_bet * outcome[1]
            if outcome[0] > 21 or outcome[0] < dealer_outcome:
                self._player_cash -= player_bet * outcome[1]
                sum -= player_bet * outcome[1]
            elif outcome[0] > dealer_outcome:
                self._player_cash += player_bet * outcome[1]
                sum += player_bet * outcome[1]
        return sum

    def _play_player_hand(self, dealer_upcard, player_hand, shoe):
        dealer_upcard = self._card_representative(dealer_upcard)
        player_total = self._calculate_total(player_hand)
        if (player_total >= 21):
            return [(player_total, 1)]
        
        if len(player_hand) == 2 and player_hand[0] == player_hand[1]:
            strategy = strategy_table['pairs'][(dealer_upcard, self._card_representative(player_hand[0]) + self._card_representative(player_hand[1]))]
        elif self._is_soft(player_hand):
            strategy = strategy_table['soft'][(dealer_upcard, str(player_total))]
        else:
            strategy = strategy_table['hard'][(dealer_upcard, str(player_total))]
        
        if strategy == 'P':
            hand1 = [player_hand[0]]
            hand1.append(shoe.draw())
            hand2 = [player_hand[1]]
            hand2.append(shoe.draw())
            results1 = self._play_player_hand(dealer_upcard, hand1, shoe)
            results2 = self._play_player_hand(dealer_upcard, hand2, shoe)
            results1.extend(results2)
            return results1
        elif strategy == 'S':
            return [(player_total, 1)]
        elif strategy == 'H' or (strategy == 'D' and len(player_hand) > 2):
            player_hand.append(shoe.draw())
            return self._play_player_hand(dealer_upcard, player_hand, shoe)
        elif strategy == 'D':
            player_hand.append(shoe.draw())
            return [(self._calculate_total(player_hand), 2)]
        
    def _play_dealer_hand(self, dealer_hand, shoe):
        """Plays the dealer's hand.

        Args:
            dealer_hand (List[Int]): The dealer's hand
            shoe (SimplifiedShoe): The shoe

        Returns:
            Int: The dealer's total
        """
        total = self._calculate_total(dealer_hand)
        if (total == 17 and not self._is_soft(dealer_hand)) or total > 17:
            return total
        dealer_hand.append(shoe.draw())
        return self._play_dealer_hand(dealer_hand, shoe)

    def _deal(self):
        """Deals a hand of blackjack.
        """
        self._player_hand = []
        self._dealer_hand = []
        self._player_hand.append(self._shoe.draw())
        self._dealer_hand.append(self._shoe.draw())
        self._player_hand.append(self._shoe.draw())
        self._dealer_hand.append(self._shoe.draw_face_down())

    def _card_representative(self, card_value):
        if card_value == 10:
            return 'T'
        elif card_value == 1:
            return 'A'
        else:
            return str(card_value)
    
    def _is_soft(self, hand):
        """Determines if a hand is soft.

        Args:
            hand (List[Int]): The hand to check

        Returns:
            Boolean: True if the hand is soft, False otherwise
        """
        total = sum(hand)
        if hand.count(1) == 0:
            return False
        else:
            return total <= 11
        
    def _calculate_total(self, hand):
        """Calculates the total value of a hand.

        Args:
            hand (List[Int]): The hand to calculate the total of

        Returns:
            Int: The total value of the hand
        """
        num_aces = hand.count(1)
        total = sum(hand)
        if num_aces == 0 or total >= 12:
            return total 
        else:
            return total + 10
        