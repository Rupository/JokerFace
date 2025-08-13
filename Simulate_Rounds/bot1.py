from win_rate import analyze_hand_vs_all_hands, RANK_ORDER
import random
from collections import Counter

#Aggresive Bot: Raises quite often, a bit hard to predict, folds if it doesn't have good cards pre-flop
#Also, doesnt care much about othe player raising, and will likely call


#Problem: Bots might keep on raising and raising against each other, so it's better to keep the amount of times you can raise per round to one





def determine_possibilities(allcards):
    ranks = [rank for rank, suit in allcards]
    suits = [suit for rank, suit in allcards]
    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)
    flush_possible = False
    is_paired_board = False

    # Determine how many pairs, trips, flush possibilities
    pairs = sum(1 for count in rank_counts.values() if count == 2)
    trips = sum(1 for count in rank_counts.values() if count == 3)
    flush_possible = any(count >= 4 for count in suit_counts.values())
    is_paired_board = any(count >= 2 for count in rank_counts.values())

    return (flush_possible, is_paired_board, pairs, trips)

def get_card_value(card):
    rank, _ = card
    return RANK_ORDER.index(rank)

class bot1:
    def __init__(self, botcards = None, botmoney = 0, standing_bet = 0, community_cards = None):
        self.botcards= botcards
        self.botmoney = botmoney
        self.standing_bet = standing_bet
        self.community_cards = community_cards

    def preflop(self, raise_possible):
        
        analysis = analyze_hand_vs_all_hands(self.botcards, 1)
        if analysis >= 0.6:
            if raise_possible == True:
                raise_possible = False
                return ('R',(int(random.uniform(0.01, 0.05) * self.botmoney)))
            else: return ('C', 0)
        elif analysis >= 0.2 and analysis < 0.6:
            return ('C', 0)
        else:
            return ('F', 0)
        

    def flop(self, raise_possible):
        allcards = self.botcards + self.community_cards
        possibilities = determine_possibilities(allcards) #Returns (flush_possible, is_paired_board, pairs, trips)
        prob = random.random()

        '''
        if self.standing_bet > (0.5 * self.botmoney):
            if prob > 0.4: #So you can't ALWAYS beat the bot by just going all in to make it fold
                return ('F', 0)'''

        if possibilities[3] >= 1:
            if raise_possible == True:
                raise_possible = False
                return ('R',(int(random.uniform(0.005, 0.1) * self.botmoney)))
            else: return ('C', 0)
        
        if possibilities[0] == True or possibilities[1] == True :
            if raise_possible == True:
                raise_possible = False
                return ('R',(int(random.uniform(0.1, 0.2) * self.botmoney)))
            else: return ('C', 0)

        #BLUFFFFFF
        if prob >= 0.5:
            if raise_possible == True:
                raise_possible = False
                return ('R',(int(random.uniform(0.01, 0.15) * self.botmoney)))
            else: return ('C', 0)
        else:
            return ['C', 0]   
        
        
    def turn(self, raise_possible):
        allcards = self.botcards + self.community_cards
        possibilities = determine_possibilities(allcards) #Returns (flush_possible, is_paired_board, pairs, trips)

        prob1 = random.random()
        if prob1 >= 0.4: #So that it doesn't continuously keep raising when it has good cards (so there is a bit of randomness)
            if possibilities[3] >= 1:
                if raise_possible == True:
                    raise_possible = False
                    return ('R',(int(random.uniform(0.05, 0.1) * self.botmoney)))
                else: return ('C', 0)
            
            if possibilities[0] == True or possibilities[1] == True :
                if raise_possible == True:
                    raise_possible = False
                    return ('R',(int(random.uniform(0.01, 0.2) * self.botmoney)))
                else: return ('C', 0)
                    
        prob2 = random.random() #BLUFFFFFF
        if prob2 >= 0.5:
            if raise_possible == True:
                raise_possible = False
                return ('R',(int(random.uniform(0.01, 0.15) * self.botmoney)))
            else: return ('C', 0)
        else:
            return ('C', 0)
        

    def river(self, raise_possible):
        allcards = self.botcards + self.community_cards
        possibilities = determine_possibilities(allcards) #Returns (flush_possible, is_paired_board, pairs, trips)

        prob1 = random.random()
        if prob1 >= 0.5:
            if possibilities[3] >= 1:
                if raise_possible == True:
                    raise_possible = False
                    return ('R',(int(random.uniform(0.005, 0.1) * self.botmoney)))
                else: return ('C', 0)
            
            if possibilities[0] == True or possibilities[1] == True :
                if raise_possible == True:
                    raise_possible = False
                    return ('R',(int(random.uniform(0.01, 0.15) * self.botmoney)))
                else: return ('C', 0)
            
            return ('C', 0)
            
        else:
            return ('C', 0)
        
                    
    
    
'''

#If you wanna test:

botcards = [('7', '♠'), ('7', '♥')]
botmoney = 100
community_cards = [('3', '♣'), ('5', '♣'), ('K', '♣')]
standing_bet = 12

print (f"Preflop: {bot1_preflop(True, botcards, botmoney)}")
raise_possible = True
print (f"Flop: {bot1_flop(True, botcards, botmoney, community_cards, standing_bet)}")
raise_possible = True
print (f"Turn: {bot1_turn(True, botcards, botmoney, community_cards)}")
raise_possible = True
print (f"River: {bot1_river(True, botcards, botmoney, community_cards)}")



'''
