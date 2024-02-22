import sys
import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import config, fetchData, processData, economics
from battery import Battery

'''Variables'''
try:
    bat = Battery.from_json("megapack.json")
except Exception as err:
    print("Failed to instantiate battery object from json file...\n")
    sys.exit(err)

#tariff = float(input("Tariff [€/MWh]: "))

containers = math.ceil(config.pv_size * 1000 * config.bess_pv_power_ratio / bat.power_w)
print("Containers: ", containers, containers * bat.power_w / 1_000_000, "MW")

curtailment_threshold = config.curtailment_percentage * config.pv_size / 1000
''''''

'''Base Case'''
raw = fetchData.pvgis(str(config.anthotopos[0]), str(config.anthotopos[1]), 0)
pv = fetchData.from_pvgis(raw) * 1.23 # Increase by a correction factor
pv_series = fetchData.to_series(pv) / 1_000_000

mcp = fetchData.from_trading("Hourly_prices_2050_blank.xlsx", config.mcp_year)
mcp_series = fetchData.to_series(mcp)
''''''
'''BtM Case'''
discharged_frame, discharged_energy, bess_market_revenues, drawn_from_pv = processData.behindTheMeter(pv, curtailment_threshold * 1_000_000, containers, mcp, False)
discharged_series = fetchData.to_series(discharged_frame)
''''''
'''Always Charged'''
solar_production = pv_series.sum()
solar_production_reduced = solar_production - (drawn_from_pv / 1_000_000)

solar_rate = solar_production * 1000 / config.pv_size
cf = solar_production / (config.pv_size * 8760 / 1000)

remained_production = np.clip(pv_series, None, curtailment_threshold)
curtailed_production = np.clip((pv_series - curtailment_threshold), 0, None).sum()

curtailed_percentage = curtailed_production / solar_production
hybrid_percentage = (solar_production_reduced - curtailed_production + discharged_energy) / solar_production
stored_percentage = curtailed_percentage - (1-hybrid_percentage)

hybrid_production = solar_production - curtailed_production - (drawn_from_pv / 1_000_000) + discharged_energy
''''''
'''Market'''
bess_earnings_market = bess_market_revenues + (remained_production * mcp_series).sum()
''''''
'''Results'''
print(f'\n{"*Results*":^85}')
print(f'{solar_rate:.2f} kWh/kWp --- {pv_series.max():.2f} MW --- CF: {cf:.1%} --- {config.mcp_year}')
print(f'{"!":-^85}\n')
print(f'Solar Production: {solar_production:,.2f} MWh')
print(f'Curtailed Production: {curtailed_production:,.2f} MWh')
print(f'Solar Production Reduced: {(drawn_from_pv / 1_000_000):,.2f} MWh')
print(f'BESS Discharge: {discharged_energy:,.2f} MWh')
print(f'Hybrid Production: {hybrid_production:,.2f} MWh')
print(f'Dumped Percentage: {(solar_production - hybrid_production) / solar_production:,.2%}')
print(f'{"!":-^85}\n')
print(f'Stored Percentage: {stored_percentage:,.2%}')
print(f'{"!":-^85}\n')
print(f'Curtailment: {1 - config.curtailment_percentage:.1%}')
print(f'Curtailed Percentage: {curtailed_percentage:.2%}')
print(f'Hybrid Percentage: {hybrid_percentage:.2%}')
print(f'{"!":-^85}\n')
''''''

'''Plot'''
plt.style.use('classic')
plt.rcParams['font.family'] = 'serif'

fig, ax1 = plt.subplots()
#ax2 = ax1.twinx()

prod_plot_max = pv_series[config.timespan].max() + 10 # Buffer
mcp_plot_max = mcp_series[config.timespan].max() + 10

# if prod_plot_max > mcp_plot_max:
#     ax1.set_ylim(0, prod_plot_max)
#     ax2.set_ylim(0, prod_plot_max)
# else:
#     ax1.set_ylim(0, mcp_plot_max)
#     ax2.set_ylim(0, mcp_plot_max)

ax1.plot(config.timespan, pv_series[config.timespan],
         color='olive', label='PV Power Output')
#ax2.plot(config.timespan, mcp_series[config.timespan],
#         color='black', linestyle='dotted', label='MCP')
ax1.bar(config.timespan, discharged_series[config.timespan],
         color='deepskyblue', label='BESS Discharge', edgecolor="deepskyblue", linewidth=2)
ax1.axhline(y=curtailment_threshold, color='tomato', linestyle='dashed', label="Curtailment")
ax1.fill_between(config.timespan, pv_series[config.timespan], curtailment_threshold,
                 where=(pv_series[config.timespan] > curtailment_threshold), interpolate=True,
                 color='darkslategrey', alpha=0.40, label='Excess Energy')

ax1.set_xlabel('Hour of the year (h)', fontsize='medium')
ax1.set_ylabel('Power (MW)', fontsize='medium')
#ax2.set_ylabel('Price (€)', fontsize='medium')
ax1.set_title('PV Production and Curtailment', fontsize='x-large')

plt.grid(which='minor', alpha=0.5)
plt.grid(which='major', alpha=1.0)
ax1.legend(loc='upper left', fontsize='x-small')
#ax2.legend(loc='upper right', fontsize='x-small')

plt.show()
''''''
