import csv
import random
from datetime import datetime, timedelta

# Fix random seed for reproducibility
random.seed(42)

def write_csv(filename, header, rows):
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
# Stores only the raw responses (without risk tolerance).
# ----------------------------
ra1_header = ["phonenumber", "datetime", "question1", "question2", "question3", "question4", "question5"]
ra1_data = []
base_dt = datetime(2023, 6, 1, 10, 0, 0)
for i in range(50):
    phone = random.choice(investor_phones)
    dt = (base_dt + timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
    answers = [random.choice(options) for _ in range(5)]
    ra1_data.append([phone, dt] + answers)

write_csv("riskassessment1.csv", ra1_header, ra1_data)

# ----------------------------
# 3. RISKASSESSMENT2 (Rubric) – 3NF
# Derive unique combinations from RiskAssessment1 and compute risk tolerance.
# Now uses "conservative", "moderate", "aggressive".
# ----------------------------
ra2_header = ["question1", "question2", "question3", "question4", "question5", "risktolerance"]
unique_risk = {}
for row in ra1_data:
    key = tuple(row[2:7])  # 5 answers from RiskAssessment1
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
# Each investor gets between 1 and 3 goals.
# Timeline between 2024 and 2030; weighted random selection for goal names.
# ----------------------------
fg_header = ["goalid", "goalname", "timeline", "amountofmoney", "phonenumber"]
fg_data = []
goal_counter = 1
weights = [40, 30, 20, 5, 5, 5, 5, 5, 5, 5]
for phone in investor_phones:
    num_goals = random.randint(1, 3)
    for j in range(num_goals):
        goalid = f"g{str(goal_counter).zfill(3)}"
        goal_counter += 1
        goalname = random.choices(goal_names, weights=weights, k=1)[0]
        timeline = str(random.randint(2024, 2030))
        amount = random.randint(30000, 1000000)
        fg_data.append([goalid, goalname, timeline, str(amount), phone])
write_csv("financialgoal.csv", fg_header, fg_data)

# ----------------------------
# 5. PORTFOLIO – 3NF
# Each financial goal gets one portfolio (1:1 relation).
# Portfolio table now has: PortfolioID, AnnualisedReturn, InvestedValue, PortfolioFee, GoalID.
# Management fee is 0.88% of the invested sum.
# AnnualisedReturn will be updated later from the performance data.
# ----------------------------
port_header = ["portfolioid", "annualisedreturn", "investedvalue", "portfoliofee", "goalid"]
port_data = []
portfolio_counter = 1
for row in fg_data:
    portfolioid = f"p{str(portfolio_counter).zfill(3)}"
    portfolio_counter += 1
    # Generate invested value similar to previous PERFORMANCE1 range.
    investedvalue = random.randint(50000, 450000)
    annualisedreturn = 0  # placeholder; will update after performance generation
    portfoliofee = round(investedvalue * 0.0088, 2)
    goalid = row[0]
    port_data.append([portfolioid, str(annualisedreturn), str(investedvalue), str(portfoliofee), goalid])
write_csv("portfolio.csv", port_header, port_data)

# ----------------------------
# 6. PERFORMANCE – Combined Table – 3NF
# For each portfolio, generate 12 monthly records in 2024.
# Each record has the portfolio's invested value (from portfolio table), a randomly
# generated gain/loss (used to compute annualreturns and dailychange) and marketvalue
# (computed as investedvalue + gainloss). The portfolio's annualisedreturn is updated
# using the latest (month 12) record's annualreturns.
# ----------------------------
def random_datetime_in_month(year, month):
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return datetime(year, month, day, hour, minute, 0)

perf_header = ["portfolioid", "datetime", "investedvalue", "annualreturns", "dailychange", "gainloss", "marketvalue"]
perf_data = []
for row in port_data:
    portfolioid = row[0]
    invested = int(row[2])   # invested value from portfolio
    latest_annualreturns = None
    for month in range(1, 13):
        dt_obj = random_datetime_in_month(2024, month)
        dt_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        gainloss = random.randint(-2000, 2000)
        # Map gainloss (-2000 to 2000) to annualreturns (-5% to +15%)
        fraction = (gainloss + 2000) / 4000.0
        annualreturns = round(-5 + (fraction * 20), 2)
        dailychange = round(random.uniform(-5, 5), 2)
        marketvalue = invested + gainloss
        perf_data.append([portfolioid, dt_str, str(invested), str(annualreturns), str(dailychange), str(gainloss), str(marketvalue)])
        if month == 12:
            latest_annualreturns = annualreturns
    # Update the portfolio's annualisedreturn with the latest annualreturns
    row[1] = str(latest_annualreturns)
    
write_csv("performance.csv", perf_header, perf_data)

# ----------------------------
# 7. ASSET – 3NF (Total asset rows = 150)
# Each portfolio gets either 1 asset (allocation = 1.0) or 2 assets (random split summing to 1).
# ----------------------------
asset_header = ["assetid", "allocationratio", "portfolioid"]
asset_data = []
num_portfolios = len(port_data)
m = 150 - num_portfolios  # number of portfolios to receive 2 assets
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
# 8. FUNDS – 3NF (subclass of Asset)
# ----------------------------
funds_header = ["assetid", "dividendyield", "expenseratio"]
funds_data = []
for aid in asset_ids[0:40]:
    dividendyield = round(random.uniform(0.02, 0.06), 3)
    expenseratio = round(random.uniform(0.01, 0.03), 3)
    funds_data.append([aid, str(dividendyield), str(expenseratio)])
write_csv("funds.csv", funds_header, funds_data)

# ----------------------------
# 9. CASH – 3NF (subclass of Asset)
# ----------------------------
cash_header = ["assetid", "cashamount", "currency"]
cash_data = []
for aid in asset_ids[40:60]:
    cashamount = random.randint(1000, 20000)
    currency = "usd"
    cash_data.append([aid, str(cashamount), currency])
write_csv("cash.csv", cash_header, cash_data)

# ----------------------------
# 10. BONDS1 – 3NF (subclass of Asset)
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
# 11. BONDS2 – 3NF (describes bonds by name)
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
# 12. COMMODITY – 3NF
# ----------------------------
commodity_header = ["assetid", "numcommodity", "commoditytype"]
commodity_data = []
for aid in asset_ids[80:100]:
    numcommodity = random.randint(1, 100)
    commoditytype = random.choice(commodity_types)
    commodity_data.append([aid, str(numcommodity), commoditytype])
write_csv("commodity.csv", commodity_header, commodity_data)

# ----------------------------
# 13. STOCKS – 3NF (subclass of Asset)
# Allocation ratio is stored in Asset; here we store stock-specific data.
# For stocks, PERatio, Ebita, and EPS are fixed per stock name while NumOfStocks varies per record.
# ----------------------------
stocks_header = ["assetid", "peratio", "stockname", "ebita", "numofstocks", "eps"]
stocks_data = []
stock_specs = {}  # Fixed values for each stock name: (peratio, ebita, eps)
for aid in asset_ids[100:150]:
    stockname = random.choice(stock_names)
    if stockname not in stock_specs:
        peratio = round(random.uniform(10.0, 35.0), 2)
        ebita = round(random.uniform(1.0, 15.0), 2)
        eps = round(random.uniform(0.5, 5.0), 2)
        stock_specs[stockname] = (peratio, ebita, eps)
    else:
        peratio, ebita, eps = stock_specs[stockname]
    numofstocks = random.randint(50, 1000)  # Varies per record
    stocks_data.append([aid, str(peratio), stockname, str(ebita), str(numofstocks), str(eps)])
write_csv("stocks.csv", stocks_header, stocks_data)

# ----------------------------
# Build mapping: Investor -> Portfolio(s)
# ----------------------------
goalid_to_phone = {}
for row in fg_data:
    goalid, _, _, _, phone = row
    goalid_to_phone[goalid] = phone

phone_to_portfolios = {}
for row in port_data:
    portfolioid, _, _, _, goalid = row
    phone = goalid_to_phone[goalid]
    phone_to_portfolios.setdefault(phone, []).append(portfolioid)

import random
from datetime import datetime, timedelta

# --------------------------------------
# CONFIG
# --------------------------------------
trans_header = ["transactionid", "transactionamount", "transactiondate", "portfolioid", "assetid"]
trans_data = []

market_tids = [f"t{str(i).zfill(3)}" for i in range(1, 301)]
rebalancing_tids = [f"t{str(i).zfill(3)}" for i in range(301, 601)]
withdrawal_tids = [f"t{str(i).zfill(3)}" for i in range(601, 901)]

# --------------------------------------
# GENERATE TRANSACTION DATA (900 total)
# --------------------------------------
all_tids = market_tids + rebalancing_tids + withdrawal_tids
base_dt = datetime(2024, 1, 1)

for t_id in all_tids:
    transactionamount = random.randint(500, 10000)
    rand_dt = base_dt + timedelta(days=random.randint(0, 364), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    transactiondate = rand_dt.strftime("%Y-%m-%d %H:%M:%S")
    portfolioid = random.choice([row[0] for row in port_data])
    assetid = random.choice(asset_ids)
    trans_data.append([t_id, str(transactionamount), transactiondate, portfolioid, assetid])

# Write TRANSACTION table
write_csv("transaction.csv", trans_header, trans_data)

# Helper maps for later use
trans_dict = {row[0]: row[3] for row in trans_data}
invested_dict = {row[0]: float(row[2]) for row in port_data}

# --------------------------------------
# MARKETTRANSACTION: t001 – t300
# --------------------------------------
mt_header = ["transactionid", "companyid"]
mt_data = []
for t_id in market_tids:
    companyid = f"brk{str(random.randint(1, 15)).zfill(3)}"
    mt_data.append([t_id, companyid])
write_csv("markettransaction.csv", mt_header, mt_data)

# --------------------------------------
# REBALANCINGTRANSACTION: t301 – t600
# --------------------------------------
rt_header = ["transactionid", "fee"]
rt_data = []
for t_id in rebalancing_tids:
    portfolioid = trans_dict.get(t_id)
    fee = round(invested_dict.get(portfolioid, 0) * 0.002, 2)
    rt_data.append([t_id, str(fee)])
write_csv("rebalancingtransaction.csv", rt_header, rt_data)

# --------------------------------------
# WITHDRAWALORTOPUPTRANSACTION: t601 – t900
# --------------------------------------
wot_header = ["transactionid", "type"]
wot_data = []
for t_id in withdrawal_tids:
    ttype = random.choice(["topup", "withdrawal"])
    wot_data.append([t_id, ttype])
write_csv("withdrawalortopuptransaction.csv", wot_header, wot_data)

# ----------------------------
# 18. POSTTRADECOMPANY – 3NF
# ----------------------------
ptc_header = ["companyid", "companyname", "region"]
ptc_data = []
for i in range(1, 16):
    cid = f"brk{str(i).zfill(3)}"
    cname = random.choice(brokerage_names)
    region = random.choice(regions)
    ptc_data.append([cid, cname, region])
write_csv("posttradecompany.csv", ptc_header, ptc_data)

# ----------------------------
# X. COMBINE RISK ASSESSMENT INTO ONE FILE
# Each record from riskassessment1 is augmented with the computed risk tolerance 
# (derived from riskassessment2) based on its answer combination.
# ----------------------------
combined_ra_header = ["phonenumber", "datetime", "question1", "question2", "question3", "question4", "question5", "risktolerance"]
combined_ra_data = []

for row in ra1_data:
    key = tuple(row[2:7])
    rt = unique_risk.get(key, "")  # Get risk tolerance; default to empty if not found (should not happen)
    combined_ra_data.append(row + [rt])

write_csv("riskassessment_combined.csv", combined_ra_header, combined_ra_data)

print("CSV files generated successfully, including 'riskassessment_combined.csv'.")
