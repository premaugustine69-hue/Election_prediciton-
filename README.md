# Election Prediction — 2026 US Midterms

A Monte Carlo election forecast for the 2026 US midterm elections (Election Day: Tuesday, November 3, 2026), built with Mercury (Muse).

## My model (frozen forecast, Nov 1, 2026)

20,000 simulations, correlated national error + per-race noise:

- **House:** Democrats 94% to win control, median 233 seats
- **Senate:** Democrats 46%, median 50 seats
- Most likely single outcome: Democratic House / Republican Senate (49%)

The model will be graded against the called results on Wednesday, November 4, 2026.

## Live page

The forecast page, refreshed every 30 minutes through election night:
https://muse.ai/s/election-prediction-xwxm6gaxnxmg4xm8/sPdLcrZ8eGuTc6du9PhJj6D--M5h6U7zuIxJoEY7_H4

## Files

- `index.html` — the forecast website (self-contained page: House & Senate predictions, USA map, forecaster comparison, simulator, Nov 3 results section)
- `election_predictor.py` — the Monte Carlo model (pure Python, race probabilities at the top of the file)

Run the model:

```bash
python3 election_predictor.py
```
