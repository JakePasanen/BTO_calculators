import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

try:
    import input_validator as inp
    import calculations as calc
    import formatter
except:
    from ev_bot import input_validator as inp
    from ev_bot import calculations as calc
    from ev_bot import formatter

TOKEN = 'MTIzNDQ5MjgzMzc4OTExNjQ2Nw.GAgvW6.J-q7xMnqyZg39dSJgkDjB7MpHM8miCdmF38i3w'
DEBUG = True

bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())

@bot.event
async def on_ready():
    print("Bot is up and ready!!")
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)


@bot.tree.command(name="ev", description="Use Probit devigging to get the EV of a bet.")
@app_commands.describe(
    payout_odds='The odds of the bet.', 
    fv_odds='The fair value odds of each leg.', 
    bet_name='[optional] Name of the bet.', 
    boost='[optional] Boost to add to the odds of the bet.')
async def ev(interaction: discord.Interaction, payout_odds: str, fv_odds: str, boost: str=None,bet_name: str = None):
    print(f'{datetime.now()} EV called by @{interaction.user.name}')
    out  = '```'
    if DEBUG:
        out += 'Debug:\n'
        out += f'  User: {interaction.user.name} ({interaction.user.mention})\n'
        out += f'  Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
        out += '\n'
    
    #############
    try:
        payout_vals, fv_vals = inp.parse_input(payout_odds, fv_odds)
    except Exception as e:
        raise(e)

    dec_odds_input = 1/payout_vals
    if boost is not None:
        boost_val,boost_type = inp.parse_boost(boost)
        dec_odds = calc.adjust_for_boost(dec_odds_input, boost_val, boost_type)
    else:
        dec_odds = dec_odds_input

    win_prob = 1
    for fv in fv_vals:
        win_prob = win_prob * fv

    fv_amer = calc.dec_to_amer( 1/win_prob )
    ev = calc.calculate_ev(win_prob, dec_odds)

    kelly_units = calc.calculate_kelly(win_prob, dec_odds, 1)*100
    
    try:
        if boost is None:    
            out += formatter.format_ev(payout_odds, dec_odds, fv_odds, win_prob, fv_amer, ev, kelly_units=kelly_units, bet_name=bet_name)    
        else:
            boosted_amer = calc.dec_to_amer(dec_odds)
            out += formatter.format_ev(payout_odds, dec_odds, fv_odds, win_prob, fv_amer, ev, kelly_units=kelly_units, bet_name=bet_name, boost=boost, boosted_odds=boosted_amer)
    except Exception as e:
        raise (e)
    
    out += '```'
    
    await interaction.response.send_message(
        out
    )
    

@bot.tree.command(name="middle", description="Calculate the optimal middle bet sizing.")
@app_commands.describe(
    side1='American odds of side 1.',
    side2='American odds of side 2.',
    total_risk='Amount in dollars that you want at risk.'
    )
async def middle(interaction: discord.Interaction, side1: str, side2: str, total_risk: str):
    out = '```'
    if DEBUG:
        out += 'Debug:\n'
        out += f'  User: {interaction.user.name} ({interaction.user.mention})\n'
        out += f'  Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
        out += '\n'
    

    odds1_amer = inp.parse_single_odd(side1)
    odds2_amer = inp.parse_single_odd(side2)
    total_bet = inp.parse_bet_size(total_risk)
    
    odds1_dec = calc.amer_to_dec(odds1_amer)
    odds2_dec = calc.amer_to_dec(odds2_amer)


    mid_odds_dec, risk1, risk2, actual_risk = calc.calculate_middle_odds(odds1_dec,odds2_dec,total_bet=total_bet)
    mid_odds_amer = calc.dec_to_amer(mid_odds_dec)
    mid_prob = 1/mid_odds_dec


    profit = (mid_odds_dec-1)*total_bet
    out += formatter.format_middle(odds1_amer, odds2_amer, mid_odds_amer, mid_prob, bet_amt=total_bet, bet1=risk1, bet2=risk2, profit=profit )

    out += '```'
    
    await interaction.response.send_message(
        out
    )
    
    

@bot.tree.command(name="arb", description="Calculate the optimal arbitrage bet sizing.")
@app_commands.describe(
    side1='American odds of side 1.',
    side2='American odds of side 2.',
    total_risk='Amount in dollars that you have available to risk.'
    )
async def arb(interaction: discord.Interaction, side1: str, side2: str, total_risk: str):
    out = '```'
    if DEBUG:
        out += 'Debug:\n'
        out += f'  User: {interaction.user.name} ({interaction.user.mention})\n'
        out += f'  Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
        out += '\n'
    

    odds1_amer = inp.parse_single_odd(side1)
    odds2_amer = inp.parse_single_odd(side2)
    total_bet  = inp.parse_bet_size(total_risk)
    
    odds1_dec = calc.amer_to_dec(odds1_amer)
    odds2_dec = calc.amer_to_dec(odds2_amer)
    
    side1_bet, side2_bet, profit = calc.calculate_arb_values(odds1_dec, odds2_dec, total_bet)
    roi = profit / total_bet
    
    out += formatter.format_arb(odds1_amer, odds2_amer, total_bet, side1_bet, side2_bet, profit, roi)

    out += '```'
    
    await interaction.response.send_message(
        out
    )
    
    
   
@bot.tree.command(name="convert_free_bet", description="Calculate free bet conversion.")
@app_commands.describe(
    free_bet_size='Size of offered free bet in dollars.',
    freebet_odds='American odds of free bet side of conversion.',
    hedge_odds='American odds of hedge side of conversion.',
    )
async def convert_free_bet(interaction: discord.Interaction, free_bet_size: str, freebet_odds: str, hedge_odds: str):
    out = '```'
    if DEBUG:
        out += 'Debug:\n'
        out += f'  User: {interaction.user.name} ({interaction.user.mention})\n'
        out += f'  Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
        out += '\n'
    
    free_amer = inp.parse_single_odd(freebet_odds)
    hedge_amer = inp.parse_single_odd(hedge_odds)
    freebet = inp.parse_bet_size(free_bet_size)
    
    free_dec = calc.amer_to_dec(free_amer)
    hedge_dec = calc.amer_to_dec(hedge_amer)

    stake, convert_rate = calc.calculate_free_bet_convert(free_dec,hedge_dec, freebet)
    profit = convert_rate*freebet
    
    out += formatter.format_freebet_convert(freebet, free_amer, hedge_amer, stake, convert_rate, profit)
    
    out += '```'
    
    await interaction.response.send_message(
        out
    ) 


    
    
bot.run(TOKEN)