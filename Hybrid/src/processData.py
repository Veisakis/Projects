'''Data manipulation functions'''

import sys
import math
import numpy as np
import pandas as pd

import fetchData, economics, config
from battery import Battery


def energyPrettify(energy):
    '''Nice format for printing energy values'''
    return format(round(energy, 2), ",") + " Wh"


def chargeExcess(production, curtailment, battery):
    '''Calculate excess energy produced and return how much is stored '''
    excess_energy = np.clip((production - curtailment), 0, None).sum()
    remained_production = np.clip(production, None, curtailment).sum()

    if (excess_energy * math.sqrt(battery.rte)) < battery.nominal_capacity:
        charge_from_curtailed = excess_energy * math.sqrt(battery.rte)
        energy_needed = (battery.nominal_capacity - charge_from_curtailed) / math.sqrt(battery.rte)

        if remained_production >= energy_needed:
            return battery.nominal_capacity, energy_needed
        else:
            return charge_from_curtailed, remained_production * math.sqrt(battery.rte)
    else:
        return battery.nominal_capacity, 0


def dichargeExcess(stored, curtailment, battery):
    '''Discharge stored energy'''
    total_energy = 0
    if (stored * math.sqrt(battery.rte) / 2) > curtailment:
        total_energy += curtailment * 2
    else:
        total_energy += stored * math.sqrt(battery.rte)
    return total_energy


def market(production_day, mcp_day, energy):
    '''Calculate earnings based on market prices'''
    pv_produces = np.logical_and(production_day, np.logical_not(np.zeros(24)))
    mcp_allow_to_sell = mcp_day * np.logical_not(pv_produces)

    m1, m2 = mcp_allow_to_sell.nlargest(2)
    i1, i2 = mcp_allow_to_sell.nlargest(2).index

    i1 -= 1
    i2 -= 1

    discharge_daily_curve = [0] * 24
    discharge_daily_curve[i1] = energy / 2
    discharge_daily_curve[i2] = energy / 2

    earnings = (discharge_daily_curve[i1] * m1 / 1_000_000) + (discharge_daily_curve[i2] * m2 / 1_000_000)
    return discharge_daily_curve, earnings


def behindTheMeter(production, curtailment, containers, mcp, merchant=False):
    '''Simulate behind-the-meter ESS'''
    battery = Battery.from_json("megapack.json")
    battery.batteryPack(containers)

    cum_charged_energy = 0
    cum_discharged_energy = 0
    cum_drawn_from_pv = 0

    merchant_earnings = 0
    discharge_daily_curve = [0] * 24

    bat_record = pd.DataFrame(index=np.arange(1), columns=np.arange(1, 25))

    for day in config.year:
        pv_day = production.iloc[day]

        charged_energy, drawn_from_pv = chargeExcess(pv_day, curtailment, battery)
        discharged_energy = dichargeExcess(charged_energy, curtailment, battery)

        if not merchant:
            earnings = 0
            for i in range(19,21):
                discharge_daily_curve[i] = discharged_energy / 2
        else:
            discharge_daily_curve, earnings = market(production.iloc[day], mcp.iloc[day], discharged_energy)
        bat_record.loc[day] = discharge_daily_curve

        merchant_earnings += earnings

        cum_charged_energy += charged_energy
        cum_discharged_energy += discharged_energy
        cum_drawn_from_pv += drawn_from_pv

    discharged_frame = bat_record / 1_000_000
    discharged_energy = cum_discharged_energy / 1_000_000

    return discharged_frame, discharged_energy, merchant_earnings, cum_drawn_from_pv

