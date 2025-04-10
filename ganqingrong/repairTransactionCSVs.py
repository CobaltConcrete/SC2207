import pandas as pd
import random

# Load all CSVs
transaction_df = pd.read_csv("transaction.csv")
withdrawal_topup_df = pd.read_csv("withdrawalortopuptransaction.csv")
market_transaction_df = pd.read_csv("markettransaction.csv")
company_df = pd.read_csv("posttradecompany.csv")

# Step 1: Remove transactionids from market_transaction_df that are in withdrawal_topup_df
market_transaction_df = market_transaction_df[
    ~market_transaction_df["transactionid"].isin(withdrawal_topup_df["transactionid"])
]

# Step 2: Find transactionids that are in transaction.csv but NOT in withdrawalortopuptransaction.csv
topup_ids = set(withdrawal_topup_df["transactionid"])
all_ids = set(transaction_df["transactionid"])
to_add_ids = all_ids - topup_ids

# Randomly assign companyid to new transactionids
new_entries = []
available_companies = company_df["companyid"].tolist()

for tid in to_add_ids:
    random_company = random.choice(available_companies)
    new_entries.append({"transactionid": tid, "companyid": random_company})

# Add the new entries
new_entries_df = pd.DataFrame(new_entries)
market_transaction_df = pd.concat([market_transaction_df, new_entries_df], ignore_index=True)

# Save the updated market transaction file
market_transaction_df.to_csv("repaired_markettransaction.csv", index=False)
