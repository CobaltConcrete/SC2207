import pandas as pd

# Load both CSVs
performance_df = pd.read_csv("performance.csv", parse_dates=["datetime"])
portfolio_df = pd.read_csv("portfolio.csv")

# Get the latest annual return for each portfolioid
latest_returns = (
    performance_df.sort_values("datetime")
    .groupby("portfolioid")
    .last()
    [["annualreturns"]]
    .rename(columns={"annualreturns": "annualisedreturn"})
)

# Update the portfolio dataframe
portfolio_df = portfolio_df.drop(columns=["annualisedreturn"]).merge(
    latest_returns, on="portfolioid", how="left"
)

# Save to new CSV
portfolio_df.to_csv("repaired_portfolio.csv", index=False)
