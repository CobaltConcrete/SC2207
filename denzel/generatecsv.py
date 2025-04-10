import csv
import random
from datetime import datetime, timedelta
import pandas as pd

# ----------------------------
# 0. CONFIGURATION
# ----------------------------
random.seed(42)

def write_csv(filename, header, rows):
    """Helper function to write rows to a CSV file with the given header."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

# ----------------------------
# HELPER DATA
# ----------------------------
first_names = [
    "john", "jane", "michael", "sarah", "david", "laura", "robert", "linda", "james", "barbara",
    "william", "elizabeth", "richard", "jennifer", "charles", "maria", "thomas", "susan",
    "christopher", "margaret", "mark", "nancy", "daniel", "patricia", "kevin", "helen"
]
last_names = [
    "smith", "doe", "johnson", "williams", "brown", "jones", "miller", "davis", "garcia", "rodriguez",
    "wilson", "martinez", "anderson", "taylor", "hernandez", "moore", "martin", "jackson",
    "thompson", "white", "hall", "lee", "scott", "green", "young", "clark"
]

goal_names = [
    "retirement", "buy a house", "college fund", "vacation", "emergency fund",
    "car purchase", "investment portfolio", "business startup", "wedding", "health fund"
]

stock_names = ["apple", "google", "amazon", "microsoft", "tesla"]

brokerage_names = [
    "charles schwab", "fidelity investments", "td ameritrade", "e*trade", "robinhood",
    "vanguard", "morgan stanley wealth management", "jpmorgan chase", "bofa securities",
    "citigroup global markets", "goldman sachs", "ubs", "credit suisse", "deutsche bank", "barclays"
]

regions = ["america", "europe", "asia", "africa", "oceania"]

commodity_types = ["gold", "silver", "oil", "wheat", "corn"]

options = ["a", "b", "c", "d", "e"]

# Base date used for generating date/times
base_dt = datetime(2023, 6, 1, 10, 0, 0)

# ----------------------------
# 1. INVESTOR – 3NF (50 rows)
# ----------------------------
investor_header = ["phonenumber", "name", "dateofbirth", "gender", "email", "annualincome", "company", "otherinformation"]
investor_data = []
existing_phones = set()

for i in range(1, 51):
    # Generate unique 8-digit phone number starting with 8 or 9
    while True:
        phone = random.choice(["8", "9"]) + str(random.randint(10**6, 10**7 - 1))
        if phone not in existing_phones:
            existing_phones.add(phone)
            break
    first = random.choice(first_names)
    last = random.choice(last_names)
    name = f"{first} {last}"
    # Birth years between 1960 and 2005
    year = random.randint(1960, 2005)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    dob = f"{year}-{month:02d}-{day:02d}"
    gender = random.choice(["m", "f"])
    email = f"{first}.{last}{i}@example.com"
    income = random.randint(30000, 200000)
    company = random.choice(["stark industries", "wayne enterprises", "acme corp", "globex corporation", "initech"])
    info = f"client {i}"
    investor_data.append([phone, name, dob, gender, email, str(income), company, info])

write_csv("investor.csv", investor_header, investor_data)
investor_phones = [row[0] for row in investor_data]

# ----------------------------
# 2. RISKASSESSMENT1 – 3NF (50 rows)
# Stores only raw responses (no risk tolerance).
# ----------------------------
ra1_header = ["phonenumber", "datetime", "question1", "question2", "question3", "question4", "question5"]
ra1_data = []
for i in range(50):
    phone = random.choice(investor_phones)
    dt = (base_dt + timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
    answers = [random.choice(options) for _ in range(5)]
    ra1_data.append([phone, dt] + answers)

write_csv("riskassessment1.csv", ra1_header, ra1_data)

# ----------------------------
# 3. RISKASSESSMENT2 (Rubric) – 3NF
# Compute "conservative", "moderate", or "aggressive" from the combos in RA1.
# ----------------------------
ra2_header = ["question1", "question2", "question3", "question4", "question5", "risktolerance"]
unique_risk = {}
for row in ra1_data:
    key = tuple(row[2:7])  # 5 answers
    count_non_a = sum(1 for ans in key if ans != "a")
    if count_non_a % 3 == 0:
        rt = "conservative"
    elif count_non_a % 3 == 1:
        rt = "moderate"
    else:
        rt = "aggressive"
    unique_risk[key] = rt
ra2_data = [list(key) + [unique_risk[key]] for key in unique_risk]

write_csv("riskassessment2.csv", ra2_header, ra2_data)

# ----------------------------
# 4. FINANCIALGOAL – 3NF
# Each investor gets between 1 and 3 goals with a timeline and a datecreated.
# ----------------------------
# Added new column 'datecreated'
fg_header = ["goalid", "goalname", "timeline", "amountofmoney", "phonenumber", "datecreated"]
fg_data = []
goal_counter = 1
weights = [40, 30, 20, 5, 5, 5, 5, 5, 5, 5]
# For simplicity, we'll set datecreated to the base date (or you can generate a random date if desired)
datecreated = base_dt.strftime("%Y-%m-%d")
for phone in investor_phones:
    num_goals = random.randint(1, 3)
    for j in range(num_goals):
        goalid = f"g{str(goal_counter).zfill(3)}"
        goal_counter += 1
        goalname = random.choices(goal_names, weights=weights, k=1)[0]
        timeline = str(random.randint(2024, 2030))
        amount = random.randint(30000, 1000000)
        fg_data.append([goalid, goalname, timeline, str(amount), phone, datecreated])
write_csv("financialgoal.csv", fg_header, fg_data)

# ----------------------------
# 5. PORTFOLIO – 3NF
# Each financial goal has one portfolio (1:1).
# We do NOT store 'investedvalue' permanently here; we only use it internally to compute performance.
# 'annualisedreturn' is a placeholder that will be corrected after performance generation.
# ----------------------------
port_header = ["portfolioid", "annualisedreturn", "portfoliofee", "goalid"]
port_data = []
portfolio_invested_map = {}  # keep track of invested value for performance generation
portfolio_counter = 1
for row in fg_data:
    portfolioid = f"p{str(portfolio_counter).zfill(3)}"
    portfolio_counter += 1
    investedvalue = random.randint(50000, 450000)  # used for performance calculations
    annualisedreturn = 0  # placeholder
    portfoliofee = round(investedvalue * 0.0088, 2)
    goalid = row[0]
    port_data.append([portfolioid, str(annualisedreturn), str(portfoliofee), goalid])
    portfolio_invested_map[portfolioid] = investedvalue

write_csv("portfolio.csv", port_header, port_data)

# ----------------------------
# 6. PERFORMANCE – single CSV
# For each portfolio, generate 12 monthly records in 2024 with columns:
#   portfolioid, datetime, investedvalue, annualreturns, dailychange, gainloss, marketvalue
# We'll then fix 'annualisedreturn' in portfolio.csv using the last record (month 12).
# ----------------------------
def random_datetime_in_month(year, month):
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return datetime(year, month, day, hour, minute, 0)

perf_header = ["portfolioid", "datetime", "investedvalue", "annualreturns", "dailychange", "gainloss", "marketvalue"]
perf_data = []

for pinfo in port_data:
    portfolioid = pinfo[0]
    invested = portfolio_invested_map[portfolioid]
    latest_annualreturns = None
    for month in range(1, 13):
        dt_obj = random_datetime_in_month(2024, month)
        dt_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        gainloss = random.randint(-2000, 2000)
        fraction = (gainloss + 2000) / 4000.0  # Maps gainloss range to 0..1
        annualreturns = round(-5 + (fraction * 20), 2)  # Annual returns from -5% to +15%
        dailychange = round(random.uniform(-5, 5), 2)
        marketvalue = invested + gainloss
        perf_data.append([
            portfolioid, dt_str, str(invested),
            str(annualreturns), str(dailychange),
            str(gainloss), str(marketvalue)
        ])
        if month == 12:
            latest_annualreturns = annualreturns
    # Update the placeholder annualisedreturn in portfolio data with the December value
    pinfo[1] = str(latest_annualreturns)

write_csv("performance.csv", perf_header, perf_data)

# ----------------------------
# 7. ASSET – 3NF
# Each portfolio gets 1 or 2 assets, summing to a total allocation ratio of 1.0.
# ----------------------------
asset_header = ["assetid", "allocationratio", "portfolioid"]
asset_data = []
num_portfolios = len(port_data)
total_asset_rows_needed = 150
m = total_asset_rows_needed - num_portfolios  # number of portfolios to get 2 assets
portfolios_with_two = set(random.sample(range(num_portfolios), m)) if m > 0 else set()

asset_counter = 1
for i, portfolio in enumerate(port_data):
    portfolioid = portfolio[0]
    if i in portfolios_with_two:
        r1 = random.random()
        r2 = 1 - r1
        asset_data.append([f"a{str(asset_counter).zfill(3)}", round(r1, 4), portfolioid])
        asset_counter += 1
        asset_data.append([f"a{str(asset_counter).zfill(3)}", round(r2, 4), portfolioid])
        asset_counter += 1
    else:
        asset_data.append([f"a{str(asset_counter).zfill(3)}", 1.0, portfolioid])
        asset_counter += 1

write_csv("asset.csv", asset_header, asset_data)
asset_ids = [row[0] for row in asset_data]

# ----------------------------
# 8. FUNDS – 3NF (subclass of asset: first 40 asset IDs)
# ----------------------------
funds_header = ["assetid", "dividendyield", "expenseratio"]
funds_data = []
for aid in asset_ids[:40]:
    dividendyield = round(random.uniform(0.02, 0.06), 3)
    expenseratio = round(random.uniform(0.01, 0.03), 3)
    funds_data.append([aid, str(dividendyield), str(expenseratio)])
write_csv("funds.csv", funds_header, funds_data)

# ----------------------------
# 9. CASH – 3NF (subclass of asset: next 20 asset IDs)
# ----------------------------
cash_header = ["assetid", "cashamount", "currency"]
cash_data = []
for aid in asset_ids[40:60]:
    cashamount = random.randint(1000, 20000)
    currency = "usd"
    cash_data.append([aid, str(cashamount), currency])
write_csv("cash.csv", cash_header, cash_data)

# ----------------------------
# 10. BONDS1 – 3NF (subclass of asset)
# ----------------------------
bonds1_header = ["assetid", "bondname", "numofbonds"]
bonds1_data = []
i = 1
for aid in asset_ids[60:80]:
    bondname = f"bond{i}"
    numofbonds = random.randint(10, 200)
    bonds1_data.append([aid, bondname, str(numofbonds)])
    i += 1
write_csv("bonds1.csv", bonds1_header, bonds1_data)

# ----------------------------
# 11. BONDS2 – 3NF (Bond details by name)
# ----------------------------
bonds2_header = ["bondname", "interestrate", "dividendyields", "maturitydate"]
bonds2_data = []
for row in bonds1_data:
    bondname = row[1]
    interestrate = round(random.uniform(1.0, 6.0), 2)
    dividendyields = round(random.uniform(0.01, 0.06), 3)
    maturitydate = f"20{random.randint(28,35)}-12-{random.randint(1,28):02d}"
    bonds2_data.append([bondname, str(interestrate), str(dividendyields), maturitydate])
write_csv("bonds2.csv", bonds2_header, bonds2_data)

# ----------------------------
# 12. COMMODITY – 3NF (subclass of asset)
# ----------------------------
commodity_header = ["assetid", "numcommodity", "commoditytype"]
commodity_data = []
for aid in asset_ids[80:100]:
    numcommodity = random.randint(1, 100)
    commoditytype = random.choice(commodity_types)
    commodity_data.append([aid, str(numcommodity), commoditytype])
write_csv("commodity.csv", commodity_header, commodity_data)

# ----------------------------
# 13. STOCKS – 3NF (subclass of asset: next 50 asset IDs)
# ----------------------------
stocks_header = ["assetid", "peratio", "stockname", "ebdta", "numofstocks", "eps"]
stocks_data = []
stock_specs = {}
for aid in asset_ids[100:150]:
    stockname = random.choice(stock_names)
    if stockname not in stock_specs:
        peratio = round(random.uniform(10.0, 35.0), 2)
        ebita = round(random.uniform(1.0, 15.0), 2)
        eps = round(random.uniform(0.5, 5.0), 2)
        stock_specs[stockname] = (peratio, ebita, eps)
    else:
        peratio, ebita, eps = stock_specs[stockname]
    numofstocks = random.randint(50, 1000)
    stocks_data.append([aid, str(peratio), stockname, str(ebita), str(numofstocks), str(eps)])
write_csv("stocks.csv", stocks_header, stocks_data)

# ----------------------------
# 14. TRANSACTION – 900 total
# (Market, Rebalancing, Withdrawal/Topup)
# ----------------------------
trans_header = ["transactionid", "transactionamount", "transactiondate", "portfolioid", "assetid"]
trans_data = []

market_tids = [f"t{str(i).zfill(3)}" for i in range(1, 301)]
rebalancing_tids = [f"t{str(i).zfill(3)}" for i in range(301, 601)]
withdrawal_tids = [f"t{str(i).zfill(3)}" for i in range(601, 901)]

# Market transactions
for t_id in market_tids:
    transactionamount = random.randint(500, 10000)
    rand_dt = base_dt + timedelta(days=random.randint(0, 364),
                                    hours=random.randint(0, 23),
                                    minutes=random.randint(0, 59))
    transactiondate = rand_dt.strftime("%Y-%m-%d %H:%M:%S")
    portfolioid = random.choice([row[0] for row in port_data])
    assetid = random.choice(asset_ids)
    trans_data.append([t_id, str(transactionamount), transactiondate, portfolioid, assetid])

# Rebalancing transactions
for t_id in rebalancing_tids:
    transactionamount = random.randint(500, 10000)
    rand_dt = base_dt + timedelta(days=random.randint(0, 364),
                                    hours=random.randint(0, 23),
                                    minutes=random.randint(0, 59))
    transactiondate = rand_dt.strftime("%Y-%m-%d %H:%M:%S")
    portfolioid = random.choice([row[0] for row in port_data])
    assetid = random.choice(asset_ids)
    trans_data.append([t_id, str(transactionamount), transactiondate, portfolioid, assetid])

# For guaranteed top-ups: ensure one fixed portfolio (first one) receives a top-up on the 1st day of each month
fixed_portfolioid = port_data[0][0]

guaranteed_topup_ids = []
withdrawal_trans_data = []

for month in range(1, 13):
    t_id = withdrawal_tids.pop(0)
    guaranteed_topup_ids.append(t_id)
    transactionamount = random.randint(500, 10000)
    # Set transactiondate to the first day of the month in 2024 with random time
    dt_obj = datetime(2024, month, 1, random.randint(0, 23), random.randint(0, 59), 0)
    transactiondate = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    # Use the fixed portfolio to ensure one investor dollar cost averages every month
    portfolioid = fixed_portfolioid
    assetid = random.choice(asset_ids)
    withdrawal_trans_data.append([t_id, str(transactionamount), transactiondate, portfolioid, assetid])

# Remaining withdrawal transactions randomly
for t_id in withdrawal_tids:
    transactionamount = random.randint(500, 10000)
    rand_dt = base_dt + timedelta(days=random.randint(0, 364),
                                    hours=random.randint(0, 23),
                                    minutes=random.randint(0, 59))
    transactiondate = rand_dt.strftime("%Y-%m-%d %H:%M:%S")
    portfolioid = random.choice([row[0] for row in port_data])
    assetid = random.choice(asset_ids)
    withdrawal_trans_data.append([t_id, str(transactionamount), transactiondate, portfolioid, assetid])

trans_data.extend(withdrawal_trans_data)
write_csv("transaction.csv", trans_header, trans_data)

# ----------------------------
# MARKETTRANSACTION (t001 – t300)
# ----------------------------
mt_header = ["transactionid", "companyid"]
mt_data = []
for t_id in market_tids:
    companyid = f"brk{str(random.randint(1, 15)).zfill(3)}"
    mt_data.append([t_id, companyid])
write_csv("markettransaction.csv", mt_header, mt_data)

# ----------------------------
# REBALANCINGTRANSACTION (t301 – t600)
# ----------------------------
rt_header = ["transactionid", "fee"]
rt_data = []
trans_dict = {row[0]: row[3] for row in trans_data}  # transactionid -> portfolioid
invested_dict = {p[0]: float(portfolio_invested_map[p[0]]) for p in port_data}  # portfolioid -> investedvalue

for t_id in rebalancing_tids:
    portfolioid = trans_dict.get(t_id)
    fee = round(invested_dict.get(portfolioid, 0) * 0.002, 2)
    rt_data.append([t_id, str(fee)])
write_csv("rebalancingtransaction.csv", rt_header, rt_data)

# ----------------------------
# WITHDRAWALORTOPUPTRANSACTION (t601 – t900)
# ----------------------------
wot_header = ["transactionid", "type"]
wot_data = []
for rec in withdrawal_trans_data:
    t_id = rec[0]
    if t_id in guaranteed_topup_ids:
        wot_data.append([t_id, "topup"])
    else:
        ttype = random.choice(["topup", "withdrawal"])
        wot_data.append([t_id, ttype])
write_csv("withdrawalortopuptransaction.csv", wot_header, wot_data)

# ----------------------------
# POSTTRADECOMPANY (If needed)
# ----------------------------
posttrade_header = ["companyid", "companyname", "region"]
pt_data = []
for i in range(1, 16):
    cid = f"brk{str(i).zfill(3)}"
    cname = random.choice(brokerage_names)
    reg = random.choice(regions)
    pt_data.append([cid, cname, reg])
write_csv("posttradecompany.csv", posttrade_header, pt_data)

# ----------------------------
# X. COMBINING RISK ASSESSMENT
# ----------------------------
combined_ra_header = ["phonenumber", "datetime", "question1", "question2", "question3", "question4", "question5", "risktolerance"]
combined_ra_data = []
for row in ra1_data:
    key = tuple(row[2:7])
    rt = unique_risk.get(key, "")
    combined_ra_data.append(row + [rt])
write_csv("riskassessment_combined.csv", combined_ra_header, combined_ra_data)

print("Base CSV files generated successfully, including 'riskassessment_combined.csv'.")

# ----------------------------
# XI. REPAIR PORTFOLIO CSV:
# Update the final 'annualisedreturn' in portfolio.csv using the last record from performance.csv
# and save the corrected file as repaired_portfolio.csv.
# ----------------------------
def repair_portfolio_csv():
    performance_df = pd.read_csv("performance.csv", parse_dates=["datetime"])
    portfolio_df = pd.read_csv("portfolio.csv")
    
    latest_returns = (
        performance_df.sort_values("datetime")
        .groupby("portfolioid")
        .last()[["annualreturns"]]
        .rename(columns={"annualreturns": "annualisedreturn"})
    )
    
    portfolio_df = portfolio_df.drop(columns=["annualisedreturn"]).merge(
        latest_returns, on="portfolioid", how="left"
    )
    
    portfolio_df.to_csv("repaired_portfolio.csv", index=False)
    print("Created 'repaired_portfolio.csv' with updated annualisedreturn.")

repair_portfolio_csv()

# ----------------------------
# XII. SPLIT PERFORMANCE CSV INTO performance1 / 2 / 3
# ----------------------------
def split_performance_csv(filename):
    """
    Reads the performance CSV file and splits it into three separate DataFrames
    for performance1, performance2, and performance3. Saves each as a new CSV.
    
    Expected Columns:
      portfolioid, datetime, investedvalue, annualreturns, dailychange, gainloss, marketvalue
    
    Outputs:
      - performance1.csv: (portfolioid, investedvalue)
      - performance2.csv: (portfolioid, datetime, annualreturns, dailychange, gainloss)
      - performance3.csv: (gainloss, investedvalue, marketvalue)
    """
    df = pd.read_csv(filename, parse_dates=["datetime"])
    df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    performance1 = df[['portfolioid', 'investedvalue']].drop_duplicates()
    performance2 = df[['portfolioid', 'datetime', 'annualreturns', 'dailychange', 'gainloss']].copy()
    performance3 = df[['gainloss', 'investedvalue', 'marketvalue']].drop_duplicates()
    
    performance1.to_csv('performance1.csv', index=False)
    performance2.to_csv('performance2.csv', index=False)
    performance3.to_csv('performance3.csv', index=False)
    
    return performance1, performance2, performance3

split_performance_csv('performance.csv')

print("Split 'performance.csv' into performance1.csv, performance2.csv, and performance3.csv.")
print("All operations completed.")
