'''Data manipulation functions'''

import sys
import math
import numpy as np
import pandas as pd

import fetchData, economics, config
from battery import Battery


def energyPrettify(energy):
    '''Pretty format for printing energy values'''
    return format(round(energy, 2), ",") + " Wh"

def simplePerformance(containers):
    '''Operate at predetermined hours'''
    battery = Battery.from_json("megapack.json")
    battery.batteryPack(containers)

    merchant_earnings = 0
    mcp_series = pd.Series([])

    charge_day_curve = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) / math.sqrt(battery.rte)
    discharge_day_curve = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]) * math.sqrt(battery.rte)

    bat_record_day = pd.DataFrame(index=np.arange(1), columns=np.arange(1, 25))
    bat_record_year = bat_record_day

    try:
        prices_raw = pd.read_excel(config.path + config.mcp_file)
    except FileNotFoundError as err:
        sys.exit(err)

    for year in config.timeline:
        print(year, economics.euro(merchant_earnings))
        mcp = fetchData.from_trading(prices_raw, year)
        mcp_series = mcp_series._append(fetchData.to_series(mcp), ignore_index=True)

        for day in config.year:
            bat_record_day.loc[day] = (discharge_day_curve - charge_day_curve) * battery.power_w / 1_000_000
            merchant_earnings += (bat_record_day.loc[day] * mcp.loc[day]).sum()

        bat_record_year = bat_record_year._append(bat_record_day, ignore_index=True)

    return merchant_earnings, fetchData.to_series(bat_record_year), mcp_series


def optimizedPerformance(containers):
    '''Operate at max/min MCP values'''
    battery = Battery.from_json("megapack.json")
    battery.batteryPack(containers)

    merchant_earnings = 0
    mcp_series = pd.Series([])

    bat_record_day = pd.DataFrame(index=np.arange(1), columns=np.arange(1, 25))
    bat_record_year = bat_record_day

    try:
        prices_raw = pd.read_excel(config.path + config.mcp_file)
    except FileNotFoundError as err:
        sys.exit(err)

    for year in config.timeline:
        print(year, economics.euro(merchant_earnings))
        mcp = fetchData.from_trading(prices_raw, year)
        mcp_series = mcp_series._append(fetchData.to_series(mcp), ignore_index=True)

        for day in config.year:

            charge_day_curve = np.zeros(24)
            discharge_day_curve = np.zeros(24)
            mcp_sorted = mcp.loc[day].argsort().reset_index(drop=True)

            for i in range(battery.duration):
                charge_day_curve[mcp_sorted[i]] = 1
                discharge_day_curve[np.flip(mcp_sorted).reset_index(drop=True)[i]] = 1

            charge_day_curve /= math.sqrt(battery.rte)
            discharge_day_curve *= math.sqrt(battery.rte)

            bat_record_day.loc[day] = (discharge_day_curve - charge_day_curve) * battery.power_w / 1_000_000
            merchant_earnings += (bat_record_day.loc[day] * mcp.loc[day]).sum()

        bat_record_year = bat_record_year._append(bat_record_day, ignore_index=True)

    return merchant_earnings, fetchData.to_series(bat_record_year), mcp_series
