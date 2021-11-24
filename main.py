from pandas.core.indexes.datetimes import date_range
from selenium import webdriver
import sys
import pandas as pd
from helpers import frac_to_decimal, payout, stakes


url = 'https://www.oddsportal.com/soccer/europe/europa-league/krasnodar-din-zagreb-Wd2uhvFH/'
stake = int(input("Input total stake (int): "))
path = 'C:/Users/craig/Downloads/chromedriver_win32_2/chromedriver.exe'
driver = webdriver.Chrome(executable_path=path)
driver.get(url)
table_xpath = '//*[@id="odds-data-table"]/div[1]/table'


def main():
    table = driver.find_elements_by_xpath(table_xpath)[0].text
    table_list = table.splitlines()
    table_dict = {}
    for idx, element in enumerate(table_list):
        if element[0].isnumeric() and element[-1].isnumeric() and '/' in element:
            if table_list[idx+1][0].isnumeric() and table_list[idx+1][-1].isnumeric() and '/' in table_list[idx+1]:
                if table_list[idx+2][0].isnumeric() and table_list[idx+2][-1].isnumeric() and '/' in table_list[idx+1]:
                    table_dict[table_list[idx-1].strip()] = [table_list[idx], table_list[idx+1], table_list[idx+2]]

    table_dict = frac_to_decimal(table_dict)
    df = pd.DataFrame(table_dict).T
    df.columns = ["home", "draw", "away"]

    df["payout"] = df.apply(lambda row: payout(row["home"], row["draw"], row["away"]), axis=1)

    max_home = df["home"].max()
    idx_home = df["home"].idxmax()
    max_draw = df["draw"].max()
    idx_draw = df["draw"].idxmax()
    max_away = df["away"].max()
    idx_away = df["away"].idxmax()

    print(df)
    print(f'\nMax profit = {(payout(max_home, max_draw, max_away)-1)*100}%')

    home_stake, draw_stake, away_stake = stakes(stake, max_home, max_draw, max_away)

    print(f'Bet Home: £{"{:.2f}".format(home_stake)} on {idx_home}')
    print(f'Bet Draw: £{"{:.2f}".format(draw_stake)} on {idx_draw}')
    print(f'Bet Away: £{"{:.2f}".format(away_stake)} on {idx_away}')

if __name__=='__main__':
    main()