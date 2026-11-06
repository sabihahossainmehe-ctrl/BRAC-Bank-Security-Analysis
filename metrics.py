"""
Recomputes the headline risk statistics for BRAC Bank PLC from the raw
price series in this repository, so the numbers in the report can be
verified independently of the spreadsheet.

Outputs: annualized return, annualized volatility, skewness, kurtosis,
and the beta of BRAC Bank against the DSEX (Dhaka Stock Exchange Broad
Index).

Note on scope: return and volatility use the full BRAC Bank series.
Beta uses only the dates on which both BRAC Bank and the DSEX traded,
so its sample is slightly smaller. Skewness and kurtosis printed here
cover the full series; the workbook computed them over a shorter slice,
so those two figures differ from the report by design.

Usage:
    python metrics.py

Requires: pandas, numpy, scipy
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

TRADING_DAYS = 250
DATA = Path(__file__).resolve().parent


def load_series() -> tuple[pd.Series, pd.DataFrame]:
    """Return BRAC Bank daily returns, and the BRAC/DSEX returns aligned on
    shared trading dates."""
    brac = (
        pd.read_csv(DATA / "bracbank_price_volume.csv", parse_dates=["date"])
        .set_index("date")["close_price_bdt"]
        .sort_index()
    )
    dsex = (
        pd.read_csv(DATA / "dsex_index.csv", parse_dates=["date"])
        .set_index("date")["dsex_close"]
        .sort_index()
    )

    brac_returns = brac.pct_change().dropna()
    paired = (
        pd.DataFrame({"brac": brac, "dsex": dsex}).dropna().pct_change().dropna()
    )
    return brac_returns, paired


def main() -> None:
    brac_returns, paired = load_series()

    daily_mean = brac_returns.mean()
    daily_std = brac_returns.std(ddof=1)

    # Ordinary least squares slope of BRAC returns on DSEX returns.
    beta, alpha, r_value, _, _ = stats.linregress(paired["dsex"], paired["brac"])

    label = "{:<40}: {:>12}"
    print(label.format("Period", f"{brac_returns.index.min():%Y-%m-%d} to "
                                 f"{brac_returns.index.max():%Y-%m-%d}"))
    print(label.format("BRAC Bank observations", f"{len(brac_returns):,}"))
    print(label.format("Paired observations (beta sample)", f"{len(paired):,}"))
    print("-" * 54)
    print(label.format("Daily average return", f"{daily_mean:.6f}"))
    print(label.format(f"Annualized return ({TRADING_DAYS} days)",
                       f"{daily_mean * TRADING_DAYS:.2%}"))
    print(label.format("Daily standard deviation", f"{daily_std:.4%}"))
    print(label.format("Annualized volatility",
                       f"{daily_std * np.sqrt(TRADING_DAYS):.2%}"))
    print("-" * 54)
    print(label.format("Skewness (full series)",
                       f"{stats.skew(brac_returns, bias=False):.4f}"))
    print(label.format("Excess kurtosis (full series)",
                       f"{stats.kurtosis(brac_returns, bias=False):.4f}"))
    print("-" * 54)
    print(label.format("Beta vs DSEX", f"{beta:.4f}"))
    print(label.format("Alpha (daily intercept)", f"{alpha:.6f}"))
    print(label.format("R-squared", f"{r_value ** 2:.4f}"))


if __name__ == "__main__":
    main()
