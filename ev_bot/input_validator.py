try:
    import calculations as calc
except:
    from ev_bot import calculations as calc
from functools import reduce

def parse_boost(booststr):
    booststr = booststr.replace('+','')
    if '%' in booststr:
        boost_val = float(booststr.replace('%',''))/100
        boost_type = '%'
    else:
        boost_val = int(booststr)
        boost_type = '+'
    
    return boost_val,boost_type


def parse_input(payoutstr, fvstr):
    payout = parse_payout(payoutstr)
    fv     = parse_fv_string(fvstr)
    return payout, fv


def parse_payout(payout_string):
    # Returns IMPLIED PROBABILITY assc with odds of payout by list of legs
    if not isinstance(payout_string, str):
        payout_string = str(payout_string)
        
    payout = payout_string.replace('+','')
    payout = payout.split(',')
    payout = [int(x) for x in payout]
    
    payout_dec  = [calc.amer_to_dec(x) for x in payout]
    payout_prob = [1/x for x in payout_dec]
    
    total_prob = reduce((lambda x, y: x * y), payout_prob)
    
    return total_prob


def parse_fv_string(fv_string):
    # Returns list of potential parlay legs
    if not isinstance(fv_string, str):
        fv_string = str(fv_string)
    
    all_legs = fv_string.split(',')
    
    leg_probs = [process_leg_to_fairvalue(leg) for leg in all_legs]
    return leg_probs

def process_leg_to_fairvalue(leg):
    leg = leg.replace('+','')
    if '/' not in leg and '|' not in leg:
        amer = int(leg)
        dec = calc.amer_to_dec(amer)
        odds = 1/dec
        return odds
    if '/' in leg:
        return process_multiway(leg)
    if '|' in leg:
        spl = leg.split('|')
        probs = [process_leg_to_fairvalue(x) for x in spl]
        p_not = 1
        for pp in probs:
            p_not = p_not * ( 1 - pp )
        
        out = 1 - p_not
        return out
        
        
def process_multiway(leg):       
    opts = leg.split('/')
    opts = [int(x) for x in opts]
    dec = [calc.amer_to_dec(x) for x in opts]
    
    devig_probs = calc.probit_devig(dec) 
    return devig_probs[0]


def parse_single_odd(odds):
    odds = odds.replace('+','')
    return int(odds)

def parse_bet_size(betsz):
    betsz = betsz.replace('$','')
    return float(betsz)