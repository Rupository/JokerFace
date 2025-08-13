import random
from collections import Counter
from itertools import combinations

RANK_ORDER = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['♠', '♥', '♦', '♣']
DECK = [(rank, suit) for rank in RANK_ORDER for suit in SUITS]

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

def compare_hands(hand1_cards, hand2_cards):
    """Compare two hands: 1 if hand1 wins, -1 if hand2 wins, 0 if tie"""
    hand1_value, _ = get_best_hand(hand1_cards)
    hand2_value, _ = get_best_hand(hand2_cards)
    
    if hand1_value > hand2_value:
        return 1
    elif hand2_value > hand1_value:
        return -1
    else:
        return 0

def simulate_head_to_head(hole_cards1, hole_cards2, n_simulations):
    """Simulate head-to-head matchup between two starting hands"""
    hand1_wins = 0
    hand2_wins = 0
    ties = 0
    
    for _ in range(n_simulations):
        deck = DECK.copy()
        random.shuffle(deck)
        
        deck.remove(hole_cards1[0])
        deck.remove(hole_cards1[1])
        deck.remove(hole_cards2[0])
        deck.remove(hole_cards2[1])
        
        community = deck[:5]
        
        hand1_all = [hole_cards1[0], hole_cards1[1]] + community
        hand2_all = [hole_cards2[0], hole_cards2[1]] + community
        
        result = compare_hands(hand1_all, hand2_all)
        
        if result == 1:
            hand1_wins += 1
        elif result == -1:
            hand2_wins += 1
        else:
            ties += 1

    return {
        'hand1_wins': hand1_wins,
        'hand2_wins': hand2_wins,
        'ties': ties,
        'hand1_win_rate': hand1_wins / n_simulations,
        'hand2_win_rate': hand2_wins / n_simulations,
        'tie_rate': ties / n_simulations
    }

def generate_all_starting_hands(mydeck):
    hands = []
    for i in range(len(mydeck)):
        for j in range(i + 1, len(mydeck)):
            hands.append((mydeck[i], mydeck[j]))
    return hands

def analyze_hand_vs_all_hands(target_hand, n_simulations):
    mydeck = DECK.copy()
    mydeck.remove(target_hand[0])
    mydeck.remove(target_hand[1])
    all_hands = generate_all_starting_hands(mydeck)
    results = []
    
    '''
    print(f"Analyzing {target_hand[0][0]}{target_hand[0][1]}{target_hand[1][0]}{target_hand[1][1]} vs all starting hands...")
    print(f"Total hands to analyze: {len(all_hands)}")
    print("=" * 60)
    '''
    
    wins = 0
    losses = 0
    ties = 0
    processed = 0
    
    for opponent_hand in all_hands:
        
        matchup_result = simulate_head_to_head(target_hand, opponent_hand, n_simulations)
        
        results.append({
            'opponent': f"{opponent_hand[0][0]}{opponent_hand[0][1]}{opponent_hand[1][0]}{opponent_hand[1][1]}",
            'target_wins': matchup_result['hand1_wins'],
            'target_win_rate': matchup_result['hand1_win_rate'],
            'opponent_wins': matchup_result['hand2_wins'],
            'ties': matchup_result['ties']
        })
        
        wins += matchup_result['hand1_wins']
        losses += matchup_result['hand2_wins'] 
        ties += matchup_result['ties']
        processed += 1
        
        '''
        if processed % 100 == 0:
            current_win_rate = wins / (wins + losses + ties) if (wins + losses + ties) > 0 else 0
            print(f"Processed {processed} hands, current overall win rate: {current_win_rate:.1%}")
            '''
    
    total_simulations = wins + losses + ties
    overall_win_rate = wins / total_simulations if total_simulations > 0 else 0
    
    '''
    
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS:")
    print(f"Total matchups analyzed: {len(results)}")
    print(f"Overall win rate vs all hands: {overall_win_rate:.1%}")
    print(f"Total wins: {wins:,}")
    print(f"Total losses: {losses:,}") 
    print(f"Total ties: {ties:,}")
    
    

    return {
        'detailed_results': results,
        'overall_win_rate': overall_win_rate,
        'total_wins': wins,
        'total_losses': losses,
        'total_ties': ties,
        'matchups_analyzed': len(results)}

    '''

    return (overall_win_rate)
    

'''
target_hand = (('A', '♠'), ('A', '♥'))
analysis = analyze_hand_vs_all_hands(target_hand, 1)

print (analysis)
'''
