def format_ev(payout, dec_odds, fv_input, win_prob, fv_line_amer, ev, boost=None, boosted_odds=None, kelly_units=None, bet_name=None):
    
    if (boost is None and boosted_odds is not None) or (boosted_odds is None and boost is not None):
        raise(ValueError())
    
    output = ''
    
    if bet_name is not None:
        output += f'{bet_name}\n\n'
        
    output += 'Input:\n'
    output += f'  Payout:     {payout}\n'
    output += f'  FV Odds:    {fv_input}\n'
    if boost is not None:
        output += f'  Boost:      {boost}\n'
        pm = "+" if boosted_odds > 0 else ""
        output += f'  BoostOdds:  {pm}{boosted_odds:0.0f}\n'
        
    output += '\n'
    
    output += 'EV Calc (Probit) '
    if ev <= 0:
        output += '🛑:\n'
    elif ev < 0.03:
        output += '🟨:\n'
    else:
        output += '✅:\n'
    
    output += f'  %EV:      {ev*100:0.1f}%\n'
    output += f'  WinProb:  {win_prob*100:0.1f}% \n'
    pm = "+" if fv_line_amer > 0 else ""
    output += f'  FairVal:  {pm}{fv_line_amer:0.0f}\n'
    
    output += '\n'
     
    if ev > 0:
        units_returned = dec_odds
        output += 'Kelly Values / Return:\n'
        output += f'  Full: {kelly_units:0.1f}u -> {kelly_units*units_returned:0.1f}u\n'
        output += f'  1/2 : {kelly_units*0.5:0.1f}u -> {kelly_units*units_returned*0.5:0.1f}u\n'
        output += f'  1/4 : {kelly_units*0.25:0.1f}u -> {kelly_units*units_returned*0.25:0.1f}u\n'
        output += f'  1/8 : {kelly_units*0.125:0.1f}u -> {kelly_units*units_returned*0.125:0.1f}u\n'
    
    return output

def format_middle_error(side1,side2):
    output = ''
          
    output +=  'Input:\n'
    output += f'  Side1:  {side1:0.0f}\n'
    output += f'  Side2:  {side2:0.0f}\n'
    output += '\n'
    output += 'This is an arbitrage opportunity! Please use the arbitrage calculator for this bet.'
    return output

def format_middle(side1,side2,mid_odds,mid_prob,bet_amt=None,bet1=None,bet2=None, profit=None): 
    output = ''
    
          
    output +=  'Input:\n'
    output += f'  Side1:  {side1:0.0f}\n'
    output += f'  Side2:  {side2:0.0f}\n'
    if bet_amt is not None:
        output += f'  Bet:    ${bet_amt:0.2f}\n'
    
    output += '\n'
    
    output += f'Middle Stats:\n'
    pm = "+" if mid_odds > 0 else ""
    output += f'  Odds:   {pm}{mid_odds:0.0f}\n'
    output += f'  Prob:   {mid_prob*100:0.1f}%\n'
        
    output += '\n'
    
    if bet_amt is not None:
        output += f'Bet Sizing:\n'
        output += f'  Side 1:  ${bet1:0.2f}\n'
        output += f'  Side 2:  ${bet2:0.2f}\n'
        output += f'  \n'
        output += f'  Risk:    ${bet_amt:0.2f}\n'
 
        output += f'  Profit:  ${profit:0.2f}\n'
        
    return output

def format_arb(side1_amer,side2_amer,total_stake,side1_bet,side2_bet,profit, roi):
    output = ''
    
          
    output +=  'Input:\n'
    output += f'  Side1:  {side1_amer:0.0f}\n'
    output += f'  Side2:  {side2_amer:0.0f}\n'
    output += f'  Stake:  {total_stake:0.0f}\n'
            
    output += '\n'

    output += f'Bet Sizing:\n'
    output += f'  Side 1:  ${side1_bet:0.2f}\n'
    output += f'  Side 2:  ${side2_bet:0.2f}\n'
    output += f'  \n'
    output += f'Risk:    ${total_stake:0.2f}\n'
    output += f'Profit:  ${profit:0.2f}\n'
    output += f'ROI:     {roi*100:0.1f}%\n'
    
    
    output += f'\n'
    output += f'WARNING:\n'
    output += f'Arbitrage can quickly lead to limits.  Try to keep bets to full dollar values.\n'
        
    return output

def format_freebet_convert(freebet, free_amer, hedge_amer, stake, convert_rate, profit):
    output = ''
          
    output +=  'Input:\n'
    output += f'  Free Odds:   {free_amer:0.0f}\n'
    output += f'  Hedge Odds:  {hedge_amer:0.0f}\n'
    output += f'  FreeBet:     {freebet:0.0f}\n'
    
    output += f'\n'
    
    output += f'Hedge Stake:   ${stake:0.2f}\n'
    output += f'Profit:        ${profit:0.2f}\n'
    output += f'Convert Rate:  {convert_rate*100:0.1f}%\n'
    
    return output
    
    