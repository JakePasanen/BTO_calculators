import numpy as np
from scipy import stats, optimize

def amer_to_dec(odds):
    if odds is None: return None
    if odds > 0:
        out = 1 + odds / 100
    else:
        out = 1 - 100 / odds
    return out

def dec_to_amer(dec):
    if dec is None: return None
    if dec >= 2.0:
        return (dec-1)*100
    return -100/(dec-1)


def calculate_ev(p_win, dec_odds):
    return p_win*(dec_odds-1) - (1-p_win)

def calculate_kelly(p_win, dec_odds, kelly_fraction):
    full_kelly = p_win - (1-p_win)/(dec_odds-1)
    return full_kelly*kelly_fraction

def probit_devig(input_list, tol: float=0.01):
    # Inputs must be DECIMAL ODDS
    # Convert raw probabilities to z scores (probits)
    probits = stats.norm.ppf([1/x for x in input_list])

    def objective(c):
        # Find constant c such that resulting probabilities sum to 1
        new_probabilities = stats.norm.cdf(probits + c)
        return np.abs(np.sum(new_probabilities) - 1)

    # Return normalized probabilities
    return stats.norm.cdf(probits + optimize.minimize_scalar(objective, tol=tol).x)

def calculate_flat_boost(odds_dec, boost):
    odds_amer = dec_to_amer(odds_dec)
    boosted_amer = odds_amer + boost
    boosted_dec  = amer_to_dec(boosted_amer)
    return boosted_dec

def calculate_percent_boost(odds_dec,boost):
    boosted_dec = 1 + (odds_dec-1)*(1+boost) 
    return boosted_dec

def adjust_for_boost(odds_dec,boost,boost_type):
    assert boost_type in ['+','%']
    
    if boost_type == '+':
        return calculate_flat_boost(odds_dec,boost)
    if boost_type == '%':
        return calculate_percent_boost(odds_dec,boost)
    

def calculate_middle_odds(side1_dec, side2_dec, total_bet):
    
    denom = (side1_dec/side2_dec) + 1
    risk1  = total_bet / denom
    risk2  = total_bet - risk1
    
    actual_risk = risk2 - (side1_dec - 1)*risk1
    to_win = (side1_dec - 1)*risk1 + (side2_dec - 1)*risk2
    
    odds_out_dec = to_win / actual_risk + 1
    
    ratio = total_bet / actual_risk
    risk1 = ratio*risk1
    risk2 = ratio*risk2
    actual_risk = total_bet
    
    return odds_out_dec, risk1, risk2, actual_risk
    
    
def calculate_arb_values(side1_dec, side2_dec, total_stake):
    # Calculation done in BreakTheOdds section of iPad notebook
    
    return1 = side1_dec
    return2 = side2_dec
    
    side1_bet = total_stake / (return1/return2 + 1)
    side2_bet = total_stake - side1_bet
    
    profit  = side1_bet * return1 - side1_bet - side2_bet
    profit2 = side2_bet * return2 - side1_bet - side2_bet
    
    return side1_bet, side2_bet, profit


def calculate_free_bet_convert(free_dec, hedge_dec, freebet_amt):
    # Calculation done in BreakTheOdds section of iPad notebook
    stake = (free_dec-1)/hedge_dec * freebet_amt
    
    on_freewin  = (free_dec - 1)*freebet_amt - stake
    on_hedgewin = hedge_dec*stake - stake
    
    convert_rate = on_freewin / freebet_amt
    
    return stake, convert_rate
    