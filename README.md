# Security Analysis and Portfolio Management — BRAC Bank PLC

Equity analysis of **BRAC Bank PLC** (ticker `BRACBANK`, Dhaka Stock Exchange), covering risk profiling, systematic risk estimation, relative valuation, and sensitivity testing over the period **January 2018 – November 2025**.

The analysis combines a return and volatility study of ~1,860 daily observations, a beta regression against the DSEX (Dhaka Stock Exchange Broad Index), a peer-group market multiplier valuation against three comparable Bangladeshi banks, and a two-way sensitivity matrix on the P/E (price-to-earnings) ratio and required rate of return.

Built in Excel and verified in Python (pandas, NumPy, SciPy).

---

## Headline findings

| Metric | Value |
|---|---|
| Annualized return | 6.78% |
| Annualized volatility | 34.37% |
| Daily standard deviation | 2.17% |
| Skewness | +1.42 (right-skewed) |
| Kurtosis | 25.61 (leptokurtic — fat tails) |
| Beta vs DSEX | 1.08 |
| Intrinsic value — industry P/E method | BDT 46.77 / share |
| Intrinsic value — discounted P/E method | BDT 58.07 / share |
| Market price (27 Nov 2025) | BDT 65.80 / share |
| Sensitivity range | BDT 56 – 75 / share |

**Conclusion:** the stock appears modestly overvalued on relative-valuation grounds, but the premium is defensible given profitability well above the peer average — ROE (return on equity) of 22.58% against an industry 18.80%, and ROA (return on assets) of 1.77% against an industry 1.34%. The recommendation is a *moderate* buy for an investor with average risk tolerance; the fat-tailed return distribution makes it a poor fit for conservative mandates.

---

## Analysis

### 1. Price and volume behaviour

![Price volume chart](figures/01-price-volume-chart.png)

Price moved between the mid-20s and high-70s (BDT) across the period, with volume spikes clustering around large price moves — consistent with news-driven and sentiment-driven repricing rather than steady drift.

![Return chart](figures/02-return-chart.png)

### 2. Return distribution

![Return distribution](figures/03-return-distribution.png)

Returns are sharply peaked with a long right tail: skewness of +1.42 and kurtosis of 25.61. Most daily returns cluster near zero, punctuated by rare large shocks in both directions. A normal-distribution risk model therefore understates tail risk here.

<details>
<summary>Frequency distribution table (20 bins)</summary>

![Frequency table](figures/04-frequency-table.png)

</details>

### 3. Systematic risk — beta

![Beta regression](figures/05-beta-regression.png)

Regressing BRAC Bank daily returns on DSEX daily returns gives **y = 1.0776x + 0.0005**, so beta ≈ 1.08. The stock moves slightly more than the market. LankaBangla Financial Portal reports a market beta of 0.96; the gap reflects a different estimation window and methodology. Both values sit close to 1, which is what theory predicts for a private commercial bank whose fortunes track domestic credit conditions.

### 4. Relative valuation — market multiplier model

![Peer market multiples](figures/06-peer-market-multiples.png)

Peer group: BRAC Bank PLC, Eastern Bank PLC, Dutch-Bangla Bank PLC, City Bank PLC — all subject to the same regulatory, macroeconomic and competitive conditions in Bangladesh.

| Bank | P/E | P/B | P/S | ROA | ROE |
|---|---|---|---|---|---|
| BRAC Bank PLC | 8.35 | 1.27 | 1.77 | 1.77% | 22.58% |
| Eastern Bank PLC | 4.69 | 0.77 | 1.42 | 1.20% | 16.80% |
| Dutch-Bangla Bank PLC | 7.83 | 0.75 | 1.33 | 0.70% | 9.60% |
| City Bank PLC | 2.87 | 0.77 | 0.93 | 1.70% | 26.20% |
| **Industry average** | **5.94** | **0.89** | **1.36** | **1.34%** | **18.80%** |

P/B is price-to-book and P/S is price-to-sales. BRAC Bank trades at a premium on all three multiples, supported by 41% revenue growth and 52% operating profit growth.

![Intrinsic value](figures/07-intrinsic-value-pe.png)

Industry P/E of 5.94 × EPS (earnings per share) of 7.88 → **intrinsic value of BDT 46.77 per share**.

<details>
<summary>Per-share metrics and peer comparison charts</summary>

![Per-share metrics](figures/08-per-share-metrics.png)
![P/E comparison](figures/09-pe-ratio-comparison.png)
![ROA and ROE comparison](figures/10-roa-roe-comparison.png)

</details>

### 5. Forecast and discounted valuation

![Historical and projections](figures/11-historical-and-projections.png)

Revenue, operating income, net profit, EPS and dividends are projected to 2030 off an average historical growth rate of 15.86%, with a terminal value set by the industry P/E.

![Present value](figures/12-pe-present-value.png)

Discounting the projected dividend stream and terminal value at a required return of 6.46% gives **BDT 58.07 per share** — higher than the simple multiple method, still below the market price of BDT 65.80.

### 6. Sensitivity analysis

![Sensitivity matrix](figures/13-sensitivity-matrix.png)

Across P/E ratios of 7–12 and required returns of 4%–9%, intrinsic value spans **BDT 55.95 to BDT 75.01**. Against the market price of BDT 65.80 the stock reads as:

- **overvalued** under conservative assumptions (low P/E, high required return)
- **fairly priced** under moderate assumptions
- **undervalued** under optimistic assumptions

Valuation here is best read as a range, not a point estimate.

---

## Repository structure

```
.
├── analysis/
│   └── metrics.py          # Recomputes risk statistics from the raw CSVs
├── data/
│   ├── BRAC_Bank_Security_Analysis_Model.xlsx   # Full working model
│   └── raw/
│       ├── bracbank_price_volume.csv            # Daily close + volume, 2018–2025
│       └── dsex_index.csv                       # DSEX daily close, 2018–2025
├── figures/                # Charts and tables exported from the model
└── report/
    └── BRAC_Bank_Security_Analysis_Report.pdf   # Full written report
```

### Workbook sheets

| Sheet | Contents |
|---|---|
| `Price volume chart` | Daily close price and traded volume |
| `Frequency` | Return bins, skewness, kurtosis |
| `BETA` | DSEX returns and the paired regression inputs |
| `Return` | Daily, average and annualized return and standard deviation |
| `BRAC Bank_Market Multiple` | Peer multiples and intrinsic value |
| `BRAC Bank_Sensitivity Analysis` | Projections, discounting, sensitivity matrix |

---

## Reproducing the risk statistics

```bash
pip install pandas numpy scipy
python analysis/metrics.py
```

This recomputes annualized return, volatility, skewness, kurtosis and beta directly from the CSVs. Return and volatility match the workbook exactly. Beta comes out at 1.12 rather than 1.08 because the script restricts the sample to dates on which both BRAC Bank and the DSEX traded; skewness and kurtosis are higher than the reported figures because the script uses the full series while the workbook computed them over a shorter slice.

---

## Methodology

- **Returns** — simple daily returns on close prices, annualized over 250 trading days.
- **Beta** — ordinary least squares regression of BRAC Bank daily returns on DSEX daily returns.
- **Relative valuation** — market multiplier model: industry average multiple applied to the company's own per-share fundamentals (Damodaran, 2012).
- **Discounted valuation** — projected dividends per share plus a terminal value from the industry P/E, discounted at the CAPM (capital asset pricing model) required return.

## Limitations

- The peer group holds only four banks, so the industry averages are sensitive to any one of them.
- Market multiples embed current sentiment and can carry mispricing forward into the valuation.
- Projections assume historical growth rates persist, which is the main source of forecast risk.
- Relative valuation does not capture firm-specific growth options, which likely explains part of the gap between intrinsic value and market price.

## Data sources

Investing.com, LankaBangla Financial Portal, Simply Wall St, Stock Analysis, and the published annual reports of BRAC Bank PLC, Eastern Bank Limited, Dutch-Bangla Bank PLC and City Bank PLC. Full citations are in the report.

## Author

**Sabiha Hossain Mehe** — BBA in Finance & MIS (Management Information Systems), BRAC University

[GitHub](https://github.com/sabihahossainmehe-ctrl) · [LinkedIn](https://www.linkedin.com/in/sabiha-hossain-mehe-6863562a0) · msabihahossain@gmail.com

Related work: [Footwear Revenue Prediction](https://github.com/sabihahossainmehe-ctrl/Footwear-Revenue-Prediction) — linear regression sales model in Python.

## Disclaimer

Academic coursework prepared for educational purposes. Not investment advice.

## License

Released under the [MIT License](LICENSE).
