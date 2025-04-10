import pandas as pd

# Load CSVs
risk_df = pd.read_csv("riskassessment_combined.csv")
investor_df = pd.read_csv("investor.csv")

# Merge based on phonenumber (left join to keep all risk assessment entries)
merged_df = risk_df.merge(investor_df, on="phonenumber", how="left")

# Save to new CSV
merged_df.to_csv("repaired_riskassessment_combined.csv", index=False)
