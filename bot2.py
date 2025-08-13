from win_rate import analyze_hand_vs_all_hands, RANK_ORDER
from bot1 import determine_possibilities
import random

'''

Got a little lazy, so the code is pretty similar to bot1, 
but this one has different values set for the probabilities so that it doesn't raise as aggresively and
it plays more conservatively.

'''

class bot2:
    def __init__(self, botcards = None, botmoney = 0, standing_bet = 0, community_cards = None):
        self.botcards= botcards
        self.botmoney = botmoney
        self.standing_bet = standing_bet
        self.community_cards = community_cards

    def preflop(self, raise_possible):

        prob = random.random()

        if prob >= 0.8: #Bluff
            if raise_possible == True:
                raise_possible = False
                return ('R',(int(random.uniform(0.01, 0.15) * self.botmoney)))
            

        analysis = analyze_hand_vs_all_hands(self.botcards, 1)
        if analysis >= 0.8:
            if raise_possible == True:
                raise_possible = False
                return ('R',(int(random.uniform(0.01, 0.05) * self.botmoney)))
            else: return ('C', 0)
        elif analysis >= 0.3 and analysis < 0.8:
            return ('C', 0)
        else:
            return ('F', 0)
        

    def flop(self, raise_possible):
        allcards = self.botcards + self.community_cards
        possibilities = determine_possibilities(allcards) #Returns (flush_possible, is_paired_board, pairs, trips)
        prob = random.random()

        '''if self.standing_bet > (0.3 * self.botmoney):
            if prob > 0.4: #So you can't ALWAYS beat the bot by just going all in to make it fold
                return ('F', 0)'''

        if prob > 0.2:
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

        if prob <= 0.1:
            return ('F', 0)
                    
        #BLUFFFFFF
        if prob >= 0.8: #Bluffs pretty rarely
            if raise_possible == True:
                raise_possible = False
                return ('R',(int(random.uniform(0.01, 0.15) * self.botmoney)))
            else: return ('C', 0)
        else:
            return ('C', 0) 
        
        
    def turn(self, raise_possible):
        allcards = self.botcards + self.community_cards
        possibilities = determine_possibilities(allcards) #Returns (flush_possible, is_paired_board, pairs, trips)

        prob1 = random.random()

        '''if self.standing_bet > (0.6 * self.botmoney):
            if prob1 > 0.4: #So you can't ALWAYS beat the bot by just going all in to make it fold
                return ('F', 0)'''
            
        if prob1 >= 0.85: #So that it doesn't continuously keep raising when it has good cards (so there is a bit of randomness)
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
                    
        if prob1 <= 0.25:
            return ('F', 0)
        
        prob2 = random.random() #BLUFFFFFF
        if prob2 >= 0.8:
            if raise_possible == True:
                raise_possible = False
                return ('R',(int(random.uniform(0.01, 0.15) * self.botmoney)))
            else: return ('C', 0)
        else:
            return ['C', 0]   
        

    def river(self, raise_possible):
        allcards = self.botcards + self.community_cards
        possibilities = determine_possibilities(allcards) #Returns (flush_possible, is_paired_board, pairs, trips)
        
        prob1 = random.random()
        '''if self.standing_bet > (0.6 * self.botmoney):
            if prob1 > 0.4: #So you can't ALWAYS beat the bot by just going all in to make it fold
                return ('F', 0)'''
            
        if prob1 >= 0.75:
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
botmoney = 1000
community_cards = [('3', '♣'), ('5', '♣'), ('K', '♣')]
standing_bet = 111

print (f"Preflop: {bot2_preflop(True, botcards, botmoney)}")
print (f"Flop: {bot2_flop(True, botcards, botmoney, community_cards, standing_bet)}")
print (f"Turn: {bot2_turn(True, botcards, botmoney, community_cards, standing_bet)}")
print (f"River: {bot2_river(True, botcards, botmoney, community_cards,standing_bet)}")

'''