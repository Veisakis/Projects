import sys
import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import config, fetchData, processData, economics
from battery import Battery

try:
    bat = Battery.from_json("megapack.json")
except Exception as err:
    print("Failed to instantiate battery object from json file...\n")
    sys.exit(err)

containers = math.ceil(config.bess_size * 1000 / bat.power_w)

print(f'Containers: {containers}')
print(f'Power: {containers * bat.power_w / 1_000_000} MW')
print(f'Capacity: {containers * bat.nominal_capacity / 1_000_000} MWh')

total_earnings, bat_series, mcp_series = processData.simplePerformance(containers)
earnings_permwhyear = total_earnings / (containers * bat.nominal_capacity / 1_000_000) / len(config.timeline)

print(f'\n{"*Results*":^85}')
print(f'BESS Total Earnings: {economics.euro(total_earnings)}')
print(f'BESS Total Earnings per MWh per year: {economics.euro(earnings_permwhyear)}')
print(f'{"!":-^85}\n')

'''Plot'''
plt.style.use('classic')
plt.rcParams['font.family'] = 'serif'

colors = ['firebrick' if power > 0 else 'silver' for power in bat_series]

plt.plot(config.timespan, mcp_series[config.timespan],
         color='black', label='MCP')
plt.bar(config.timespan, bat_series[config.timespan],
         color=colors, edgecolor='none', label='BESS', linewidth=2, width=1)

plt.xlabel('Hour of the year (h)', fontsize='medium')
plt.ylabel('MCP (€)', fontsize='medium')
plt.title('Merchant BESS Refinery', fontsize='x-large')

plt.ylim(top=180)

plt.grid(which='minor', alpha=0.5)
plt.grid(which='major', alpha=1.0)
plt.legend(loc='upper left', fontsize='x-small')

plt.tight_layout()
plt.show()
''''''
