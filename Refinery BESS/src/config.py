import os

mcp_file = "Hourly_prices_2050.xlsx"
bess_size =  20_000

year = range(365)
timeline = range(2024, 2040)

plotDay_start = 240
plotDay_end = 250
timespan = range(24*plotDay_start, 24*plotDay_end)

path = ""

