import os

'''MORE'''
pv_size = 240_000 # PV-GIS's input is in kW
pv_production_file = "pv_production_kourkouteika_240.csv"
curtailment_percentage = 0.72
bess_pv_power_ratio =  1/4
mcp_year = 2024 # If false, use 2024 with the blank file
''''''

batSearch_start = 1
batSearch_end = 500

year = range(365)
plotDay_start = 240
plotDay_end = 250
timespan = range(24*plotDay_start, 24*plotDay_end)

discount_rate = 0.06
project_lifetime = 25

onm = 0.01
wh_sell_price = 0.0002
pv_cost_perkWp = 1_000
wt_cost_perMWp = 1_000_000

loss = "14"
angle = "30"
endyear = "2014"
startyear = "2014"

carbon_tperwh = 0.000000623
path = ""

ioannina = (39.684, 20.749)
theba = (38.4438, 23.1272)

sofades = (39.337, 22.166)
anthotopos = (40.334, 21.678)
paliochori = (40.044, 21.692)
mavrodendri = (40.377, 21.768)
alistrati = (41.067, 23.982)
kormista = (40.981, 24.057)
spilaio = (41.044, 24.053)
thimaria = (40.359, 21.957)
messaio = (40.793, 22.862)
nikopoli = (40.327, 21.748)
argilos = (40.264, 21.745)
psilorachi = (39.049, 22.955)
kourkouteika = (40.449, 21.572)

place_coordinates = {
    1: (35.512, 24.012),
    2: (35.364, 24.471),
    3: (35.343, 25.153),
    4: (35.185, 25.706),
    5: (35.050, 24.877),
    6: (35.008, 25.739),
    7: (35.204, 26.098)
}

place_name = {
    1: "chania",
    2: "rethymno",
    3: "hrakleio",
    4: "agnikolaos",
    5: "moires",
    6: "ierapetra",
    7: "shteia"
}
