"""
Election Predictor — a fast Monte Carlo forecast for the 2026 US midterms.
Built 2026-11-01, two days before Election Day (Tue Nov 3, 2026).

How it works (same basic recipe as Decision Desk HQ / Poliwave):
  1. Each race starts from a win probability based on today's public
     forecasts (DDHQ, Cook Political Report, prediction markets).
  2. Probabilities are converted to expected vote margins.
  3. The election is simulated 20,000 times. Every simulation draws:
       - one SHARED national polling error (if polls miss, they tend
         to miss the same direction everywhere), plus
       - a separate error for each race.
  4. We count how often each party wins each chamber.

Senate math: current Senate is 53 R / 47 D. 35 seats are up in 2026
(22 Republican-held, 13 Democrat-held). 65 seats are NOT up:
31 R + 34 D are locked in before a single vote is counted.
"""

import random
from statistics import NormalDist, median

random.seed(2026)
NORM = NormalDist()
SIMS = 20_000

# ---------------------------------------------------------------- Senate
# (race, party that holds the seat now, Dem win probability today)
# Probabilities are approximations from DDHQ / Cook ratings / market
# prices as of Nov 1, 2026 -- swap in your own numbers and rerun.
SENATE_RACES = [
    # Democrat-held seats (13) -- probability Democrats HOLD
    ("Colorado",        "D", 0.97),
    ("Delaware",        "D", 0.97),
    ("Illinois",        "D", 0.97),
    ("Massachusetts",   "D", 0.98),
    ("Minnesota",       "D", 0.88),
    ("New Hampshire",   "D", 0.80),
    ("New Jersey",      "D", 0.96),
    ("New Mexico",      "D", 0.96),
    ("Oregon",          "D", 0.97),
    ("Rhode Island",    "D", 0.98),
    ("Virginia",        "D", 0.90),
    ("Georgia",         "D", 0.72),   # Ossoff -- competitive hold
    ("Michigan",        "D", 0.68),   # open seat -- competitive hold
    # Republican-held seats (22) -- probability Democrats FLIP
    ("Alabama",         "R", 0.02),
    ("Arkansas",        "R", 0.03),
    ("Idaho",           "R", 0.02),
    ("Kentucky",        "R", 0.05),
    ("Louisiana",       "R", 0.03),
    ("Mississippi",     "R", 0.03),
    ("Montana",         "R", 0.10),
    ("Nebraska",        "R", 0.03),
    ("Oklahoma",        "R", 0.02),
    ("South Dakota",    "R", 0.02),
    ("Tennessee",       "R", 0.03),
    ("West Virginia",   "R", 0.02),
    ("Wyoming",         "R", 0.01),
    ("Florida (special)", "R", 0.12),
    ("Kansas",          "R", 0.32),   # lean R
    ("South Carolina",  "R", 0.28),   # toss-up per Fox rankings
    ("Texas",           "R", 0.40),   # toss-up
    ("Iowa",            "R", 0.47),   # dead heat: polling avg R +0.1
    ("North Carolina",  "R", 0.50),   # toss-up
    ("Maine",           "R", 0.55),   # Collins vs Jackson
    ("Alaska",          "R", 0.62),   # leans D in most models
    ("Ohio (special)",  "R", 0.65),   # Sherrod Brown -- lean D
]
DEM_NOT_UP = 34   # Democratic seats not on the ballot in 2026
RACE_SD = 4.2     # typical total polling error per Senate race (points)

# ----------------------------------------------------------------- House
# RealClearPolling generic-ballot average, Nov 1: Democrats +8.3.
# Seats mapping (simplified seats-votes curve, adjusted for the 2026
# mid-decade redistricting that helps Republicans ~4 seats):
#   Dem seats ~= 205 + 3.4 x (national Dem margin)
GENERIC_BALLOT_D = 8.3

senate_dem_seats = []
house_dem_seats = []
race_wins = {name: 0 for name, _, _ in SENATE_RACES}
outcomes = {"D sweep": 0, "D House / R Senate": 0,
            "R House / D Senate": 0, "R sweep": 0}

# Pre-convert each race's probability to an expected margin (points).
race_margins = [(name, NORM.inv_cdf(p) * RACE_SD) for name, _, p in SENATE_RACES]

for _ in range(SIMS):
    # One shared national error per simulated election.
    national_error = random.gauss(0, 2.0)

    # Senate
    dem_total = DEM_NOT_UP
    for name, margin in race_margins:
        sim_margin = margin + national_error + random.gauss(0, 3.7)
        if sim_margin > 0:
            dem_total += 1
            race_wins[name] += 1
    senate_dem_seats.append(dem_total)

    # House: same national error feeds the national vote, plus its own noise.
    house_margin = GENERIC_BALLOT_D + national_error + random.gauss(0, 2.2)
    house_seats = round(205 + 3.4 * house_margin)
    house_dem_seats.append(house_seats)

    d_senate = dem_total >= 51
    d_house = house_seats >= 218
    if d_senate and d_house:
        outcomes["D sweep"] += 1
    elif d_house:
        outcomes["D House / R Senate"] += 1
    elif d_senate:
        outcomes["R House / D Senate"] += 1
    else:
        outcomes["R sweep"] += 1

pct = lambda x: f"{100 * x / SIMS:.0f}%"

print(f"=== 2026 MIDTERM FORECAST — {SIMS:,} simulations ===\n")

print("SENATE")
print(f"  P(Democrats win Senate) : {pct(sum(1 for s in senate_dem_seats if s >= 51))}")
print(f"  Median Dem seats        : {median(senate_dem_seats):.0f}  (51 needed)")
print("  Closest races (Dem win % in sims):")
for name, holder, p in SENATE_RACES:
    w = race_wins[name] / SIMS
    if 0.15 < w < 0.85:
        tag = "hold" if holder == "D" else "flip chance"
        print(f"    {name:<20} {100*w:>4.0f}%   ({tag})")

print("\nHOUSE")
print(f"  P(Democrats win House)  : {pct(sum(1 for s in house_dem_seats if s >= 218))}")
print(f"  Median Dem seats        : {median(house_dem_seats):.0f}  (218 needed)")

print("\nCONTROL OF CONGRESS")
for k, v in outcomes.items():
    print(f"  {k:<22} {pct(v)}")
