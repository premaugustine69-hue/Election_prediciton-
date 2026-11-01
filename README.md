# 🗳️ Election Prediction — 2026 US Midterms

[![Live Site](https://img.shields.io/badge/Live%20Site-GitHub%20Pages-blue)](https://premaugustine69-hue.github.io/Election_prediciton-/)
![Python](https://img.shields.io/badge/Model-Python%203-green)

A Monte Carlo election forecast for the **2026 US midterm elections** (Election Day: **Tuesday, November 3, 2026**) — all 435 House seats and 35 Senate seats — with a live forecast page that refreshes every 30 minutes through election night.

## 🌐 Live site

**[premaugustine69-hue.github.io/Election_prediciton-](https://premaugustine69-hue.github.io/Election_prediciton-/)**

Also mirrored here: [Muse shared page](https://muse.ai/s/election-prediction-xwxm6gaxnxmg4xm8/sPdLcrZ8eGuTc6du9PhJj6D--M5h6U7zuIxJoEY7_H4)

## 📊 My model — frozen forecast (Nov 1, 2026)

20,000 simulations with correlated national error and per-race noise:

| Chamber | Win probability | Median seats |
|---|---|---|
| House | **Democrats 94%** | 233 |
| Senate | Democrats 46% | 50 |

Most likely single outcome: **Democratic House / Republican Senate (49%)**.

The model is frozen as the official forecast and will be graded against the called results on **Wednesday, November 4, 2026** — chamber calls, seat counts vs. medians, and the close Senate races.

## 🔄 How the page stays current

Every 30 minutes the page is rebuilt with the latest published numbers from Sikt Intelligence, VotePredictor, Poliwave, Decision Desk HQ, and the Polymarket/Kalshi markets — and on election night, with called results as they come in. Consensus at launch: House 88% Dem, Senate 62% Dem. My model's own numbers never change; they are the forecast being graded.

## 📁 Files

- `index.html` / `docs/index.html` — the forecast website (self-contained: House & Senate predictions, USA map, forecaster comparison, simulator, Nov 3 results section)
- `election_predictor.py` — the Monte Carlo model (pure Python; race probabilities are listed at the top of the file)

## ▶️ Run the model

```bash
python3 election_predictor.py
```

Built with Mercury (Muse).
