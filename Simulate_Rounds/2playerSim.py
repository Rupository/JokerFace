from bot1 import bot1
from bot2 import bot2
from win_rate import DECK, SUITS, RANK_ORDER
import random
from collections import Counter
from itertools import combinations



def get_hand_value(cards):
    """Return detailed hand value for precise comparison"""
    ranks = [card[0] for card in cards]
    suits = [card[1] for card in cards]
    
    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)
    
    # Get rank values (2=0, A=12)
    rank_values = [RANK_ORDER.index(r) for r in ranks]
    unique_ranks = sorted(list(set(rank_values)), reverse=True)
    
    # Sort ranks by frequency then by value
    sorted_by_count = sorted(rank_counts.items(), key=lambda x: (x[1], RANK_ORDER.index(x[0])), reverse=True)
    
    # Check flush
    flush = len(set(suits)) == 1
    
    # Check straight
    straight = False
    straight_high = 0
    if len(unique_ranks) == 5:
        # Normal straight
        if unique_ranks[0] - unique_ranks[4] == 4:
            straight = True
            straight_high = unique_ranks[0]
        # Ace-low straight (A-2-3-4-5)
        elif set(unique_ranks) == {12, 3, 2, 1, 0}:
            straight = True
            straight_high = 3  # 5-high straight
    
    # Royal flush (A-K-Q-J-10 suited)
    if flush and straight and straight_high == 12:
        return (9, [12])
    
    # Straight flush
    if flush and straight:
        return (8, [straight_high])
    
    # Four of a kind
    if sorted_by_count[0][1] == 4:
        quad_rank = RANK_ORDER.index(sorted_by_count[0][0])
        kicker = RANK_ORDER.index(sorted_by_count[1][0])
        return (7, [quad_rank, kicker])
    
    # Full house
    if sorted_by_count[0][1] == 3 and sorted_by_count[1][1] == 2:
        trips_rank = RANK_ORDER.index(sorted_by_count[0][0])
        pair_rank = RANK_ORDER.index(sorted_by_count[1][0])
        return (6, [trips_rank, pair_rank])
    
    # Flush
    if flush:
        return (5, unique_ranks)
    
    # Straight
    if straight:
        return (4, [straight_high])
    
    # Three of a kind
    if sorted_by_count[0][1] == 3:
        trips_rank = RANK_ORDER.index(sorted_by_count[0][0])
        kickers = sorted([RANK_ORDER.index(sorted_by_count[1][0]), 
                         RANK_ORDER.index(sorted_by_count[2][0])], reverse=True)
        return (3, [trips_rank] + kickers)
    
    # Two pair
    if sorted_by_count[0][1] == 2 and sorted_by_count[1][1] == 2:
        pair1 = RANK_ORDER.index(sorted_by_count[0][0])
        pair2 = RANK_ORDER.index(sorted_by_count[1][0])
        kicker = RANK_ORDER.index(sorted_by_count[2][0])
        return (2, sorted([pair1, pair2], reverse=True) + [kicker])
    
    # One pair
    if sorted_by_count[0][1] == 2:
        pair_rank = RANK_ORDER.index(sorted_by_count[0][0])
        kickers = sorted([RANK_ORDER.index(sorted_by_count[1][0]),
                         RANK_ORDER.index(sorted_by_count[2][0]),
                         RANK_ORDER.index(sorted_by_count[3][0])], reverse=True)
        return (1, [pair_rank] + kickers)
    
    # High card
    return (0, unique_ranks)

def get_best_hand(cards):
    """Get the best 5-card hand from 7 cards"""
    best_value = (-1, [])
    best_cards = None
    
    for five_cards in combinations(cards, 5):
        value = get_hand_value(list(five_cards))
        if value > best_value:
            best_value = value
            best_cards = five_cards
    
    return best_value, best_cards

def compare_hands(bot1_cards, bot2_cards):
    """Compare two hands: 1 if hand1 wins, -1 if hand2 wins, 0 if tie"""
    bot1_value, _ = get_best_hand(bot1_cards)
    bot2_value, _ = get_best_hand(bot2_cards)
    
    if bot1_value > bot2_value:
        return 1
    elif bot2_value > bot1_value:
        return 2
    else:
        return 0

'''
Preflop: 
Players receive their cards
They choose to raise, call/check or fold
At the end of the round, deduct from their bank accordingly
set standing bet back to zero
set raise_possible for both bots to True

'''
def deal_cards(numcards):
    deck = DECK.copy()
    random.shuffle(deck)
    return [deck.pop() for _ in range(numcards)]

Bot1 = bot1(botmoney = 1000)
Bot2 = bot2(botmoney = 1000)

bot1_wins = 0
bot2_wins = 0

bot1_folds = 0
bot2_folds = 0

ties = 0



#Play_rounds returns: (bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties)
def play_round(bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties):
    global Bot1, Bot2
    cards = deal_cards(9)
    Bot1.botcards = cards[0:2]
    Bot2.botcards = cards[2:4]
    community_cards = cards[4:9]
    pot = 0



    #Prefloppppp

    standing_bet = 50
    Bot1_action = Bot1.preflop(raise_possible=True)

    if Bot1_action[0] == 'R':
        
        standing_bet = standing_bet + Bot1_action[1]
        Bot2_action = Bot2.preflop(raise_possible=True)
        if Bot2_action[0] == 'R':
            standing_bet = standing_bet + Bot2_action[1]
            Bot1_action = Bot1.preflop(raise_possible=False)
            
            if Bot1_action[0] == 'F':
                bot1_folds = bot1_folds + 1
                bot2_wins = bot2_wins + 1
                
                return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
            else:
                Bot1.botmoney = Bot1.botmoney - standing_bet
                Bot2.botmoney = Bot2.botmoney - standing_bet
                pot = pot + (standing_bet * 2)

        elif Bot2_action[0] == 'F':
            bot2_folds = bot2_folds + 1
            bot1_wins = bot1_wins + 1
            return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
        
        else: 
            Bot1.botmoney = Bot1.botmoney - standing_bet
            Bot2.botmoney = Bot2.botmoney - standing_bet
            pot = pot + (standing_bet * 2)

    elif Bot1_action[0] == 'F':
        bot1_folds = bot1_folds + 1
        bot2_wins = bot2_wins + 1
        return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
    
    else:
        Bot2_action = Bot2.preflop(raise_possible=True)
        if Bot2_action[0] == 'R':
            standing_bet = standing_bet + Bot2_action[1]
            Bot1_action = Bot1.preflop(raise_possible=False)
            
            if Bot1_action[0] == 'F':
                bot1_folds = bot1_folds + 1
                bot2_wins = bot2_wins + 1
                return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
            else:
                Bot1.botmoney = Bot1.botmoney - standing_bet
                Bot2.botmoney = Bot2.botmoney - standing_bet
                pot = pot + (standing_bet * 2)

        elif Bot2_action[0] == 'F':
            bot2_folds = bot2_folds + 1
            bot1_wins = bot1_wins + 1
            return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
        
        else: 
            Bot1.botmoney = Bot1.botmoney - standing_bet
            Bot2.botmoney = Bot2.botmoney - standing_bet
            pot = pot + (standing_bet * 2)

    #Floppp

    standing_bet = 0
    Bot1.community_cards = community_cards[0:3]
    Bot2.community_cards = community_cards[0:3]

    Bot1_action = Bot1.flop(raise_possible=True)

    if Bot1_action[0] == 'R':
        
        standing_bet = standing_bet + Bot1_action[1]
        Bot2_action = Bot2.flop(raise_possible=True)
        if Bot2_action[0] == 'R':
            standing_bet = standing_bet + Bot2_action[1]
            Bot1_action = Bot1.flop(raise_possible=False)
            
            if Bot1_action[0] == 'F':
                bot1_folds = bot1_folds + 1
                bot2_wins = bot2_wins + 1
                
                return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
            else:
                Bot1.botmoney = Bot1.botmoney - standing_bet
                Bot2.botmoney = Bot2.botmoney - standing_bet
                pot = pot + (standing_bet * 2)

        elif Bot2_action[0] == 'F':
            bot2_folds = bot2_folds + 1
            bot1_wins = bot1_wins + 1
            return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
        
        else: 
            Bot1.botmoney = Bot1.botmoney - standing_bet
            Bot2.botmoney = Bot2.botmoney - standing_bet
            pot = pot + (standing_bet * 2)

    elif Bot1_action[0] == 'F':
        bot1_folds = bot1_folds + 1
        bot2_wins = bot2_wins + 1
        return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
    
    else:
        Bot2_action = Bot2.flop(raise_possible=True)
        if Bot2_action[0] == 'R':
            standing_bet = standing_bet + Bot2_action[1]
            Bot1_action = Bot1.flop(raise_possible=False)
            
            if Bot1_action[0] == 'F':
                bot1_folds = bot1_folds + 1
                bot2_wins = bot2_wins + 1
                return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
            else:
                Bot1.botmoney = Bot1.botmoney - standing_bet
                Bot2.botmoney = Bot2.botmoney - standing_bet
                pot = pot + (standing_bet * 2)

        elif Bot2_action[0] == 'F':
            bot2_folds = bot2_folds + 1
            bot1_wins = bot1_wins + 1
            return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
        
        else: 
            Bot1.botmoney = Bot1.botmoney - standing_bet
            Bot2.botmoney = Bot2.botmoney - standing_bet
            pot = pot + (standing_bet * 2)

    #Turn

    standing_bet = 0
    Bot1.community_cards = community_cards[0:4]
    Bot2.community_cards = community_cards[0:4]

    Bot1_action = Bot1.turn(raise_possible=True)

    if Bot1_action[0] == 'R':
        
        standing_bet = standing_bet + Bot1_action[1]
        Bot2_action = Bot2.turn(raise_possible=True)
        if Bot2_action[0] == 'R':
            standing_bet = standing_bet + Bot2_action[1]
            Bot1_action = Bot1.turn(raise_possible=False)
            
            if Bot1_action[0] == 'F':
                bot1_folds = bot1_folds + 1
                bot2_wins = bot2_wins + 1
                
                return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
            else:
                Bot1.botmoney = Bot1.botmoney - standing_bet
                Bot2.botmoney = Bot2.botmoney - standing_bet
                pot = pot + (standing_bet * 2)

        elif Bot2_action[0] == 'F':
            bot2_folds = bot2_folds + 1
            bot1_wins = bot1_wins + 1
            return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
        
        else: 
            Bot1.botmoney = Bot1.botmoney - standing_bet
            Bot2.botmoney = Bot2.botmoney - standing_bet
            pot = pot + (standing_bet * 2)

    elif Bot1_action[0] == 'F':
        bot1_folds = bot1_folds + 1
        bot2_wins = bot2_wins + 1
        return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
    
    else:
        Bot2_action = Bot2.turn(raise_possible=True)
        if Bot2_action[0] == 'R':
            standing_bet = standing_bet + Bot2_action[1]
            Bot1_action = Bot1.turn(raise_possible=False)
            
            if Bot1_action[0] == 'F':
                bot1_folds = bot1_folds + 1
                bot2_wins = bot2_wins + 1
                return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
            else:
                Bot1.botmoney = Bot1.botmoney - standing_bet
                Bot2.botmoney = Bot2.botmoney - standing_bet
                pot = pot + (standing_bet * 2)

        elif Bot2_action[0] == 'F':
            bot2_folds = bot2_folds + 1
            bot1_wins = bot1_wins + 1
            return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
        
        else: 
            Bot1.botmoney = Bot1.botmoney - standing_bet
            Bot2.botmoney = Bot2.botmoney - standing_bet
            pot = pot + (standing_bet * 2)

    #River

    Bot1_action = Bot1.river(raise_possible=True)

    if Bot1_action[0] == 'R':
        
        standing_bet = standing_bet + Bot1_action[1]
        Bot2_action = Bot2.river(raise_possible=True)
        if Bot2_action[0] == 'R':
            standing_bet = standing_bet + Bot2_action[1]
            Bot1_action = Bot1.river(raise_possible=False)
            
            if Bot1_action[0] == 'F':
                bot1_folds = bot1_folds + 1
                bot2_wins = bot2_wins + 1
                
                return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
            else:
                Bot1.botmoney = Bot1.botmoney - standing_bet
                Bot2.botmoney = Bot2.botmoney - standing_bet
                pot = pot + (standing_bet * 2)

        elif Bot2_action[0] == 'F':
            bot2_folds = bot2_folds + 1
            bot1_wins = bot1_wins + 1
            return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
        
        else: 
            Bot1.botmoney = Bot1.botmoney - standing_bet
            Bot2.botmoney = Bot2.botmoney - standing_bet
            pot = pot + (standing_bet * 2)

    elif Bot1_action[0] == 'F':
        bot1_folds = bot1_folds + 1
        bot2_wins = bot2_wins + 1
        return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
    
    else:
        Bot2_action = Bot2.river(raise_possible=True)
        if Bot2_action[0] == 'R':
            standing_bet = standing_bet + Bot2_action[1]
            Bot1_action = Bot1.river(raise_possible=False)
            
            if Bot1_action[0] == 'F':
                bot1_folds = bot1_folds + 1
                bot2_wins = bot2_wins + 1
                return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
            else:
                Bot1.botmoney = Bot1.botmoney - standing_bet
                Bot2.botmoney = Bot2.botmoney - standing_bet
                pot = pot + (standing_bet * 2)

        elif Bot2_action[0] == 'F':
            bot2_folds = bot2_folds + 1
            bot1_wins = bot1_wins + 1
            return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]
        
        else: 
            Bot1.botmoney = Bot1.botmoney - standing_bet
            Bot2.botmoney = Bot2.botmoney - standing_bet
            pot = pot + (standing_bet * 2)

    
    winner = compare_hands(Bot1.botcards + community_cards, Bot2.botcards + community_cards)
    if winner == 1:
        bot1_wins += 1
    elif winner == 2:
        bot2_wins += 1
    elif winner == 0:
        ties += 1

    '''
    print (f"Bot 1 cards: {Bot1.botcards}")
    print (f"Community cards: {Bot1.community_cards}")
    print (f"Bot 2 cards: {Bot2.botcards}")
'''



    return (bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties)





    






















    return [bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties]


        
num_rounds = int(input("Number of rounds: ")) #Add validation to make sure this isn't negative or zero
current_round = 0

while current_round != num_rounds:
    bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties = play_round(bot1_wins, bot2_wins, bot1_folds, bot2_folds, ties)
    current_round += 1

print (f"bot1_wins = {bot1_wins}, bot2_wins = {bot2_wins}")
print (f"bot1_folds = {bot1_folds}, bot2_folds = {bot2_folds}")
print (f"ties = {ties}")


