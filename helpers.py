def frac_to_decimal(bettingdict):
    for key in bettingdict:
        for i in range(len(bettingdict[key])):
            try:
                bettingdict[key][i] = bettingdict[key][i].strip().split('/')
                bettingdict[key][i] = float(bettingdict[key][i][0]) / float(bettingdict[key][i][1]) + 1
            except:
                print('Error at', key, i)
                pass
    return bettingdict

def payout(h, x, a):
    return 1/(1/h + 1/x + 1/a)

def margin(h, x, a):
    return 1/h + 1/x + 1/a

def stakes(stake, max_home, max_draw, max_away):
    home_prob = 1/max_home
    draw_prob = 1/max_draw
    away_prob = 1/max_away
    total_margin = margin(max_home, max_draw, max_away)
    stake_over_margin = stake/total_margin
    return stake_over_margin*home_prob, stake_over_margin*draw_prob, stake_over_margin*away_prob
