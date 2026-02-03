import yfinance as yf
import pandas as pd
import numpy as np
import os
import datetime

ticker = yf.Ticker("SPY")

hist = ticker.history(period="5d")

if not hist.empty:
    hist.index = hist.index.tz_convert(None).normalize()
    today = hist.index[-1]
    spot_price = hist["Close"].iloc[-1]
    print(f"Reference Spot Price: {spot_price:.2f} (Date: {today.date()})")
else:
    raise ValueError("Could not find history data.")

all_options_list = []
options = ticker.options
print(f"Found {len(options)} expiration dates. Fetching chains...")

r = 0.030 
div_yld = ticker.info.get("dividendYield", 0.0) or 0.0

for option in options:
    try:
        chain = ticker.option_chain(option)
    except Exception as e:
        print(f"Skipping expiration {option} due to error: {e}")
        continue
        
    calls = chain.calls.copy()
    calls["options_type"] = "call"
    
    puts = chain.puts.copy()
    puts["options_type"] = "put"
    
    cycle_df = pd.concat([calls, puts])
    
    cycle_df["mid"] = 0.5 * (cycle_df["bid"] + cycle_df["ask"])
    expiration_date = pd.Timestamp(option)
    
    T = (expiration_date - today).days / 365.0
    
    if T <= 0:
        continue

    cycle_df["expiration_date"] = expiration_date
    cycle_df["days_to_expiration"] = (expiration_date - today).days
    cycle_df["T"] = T
    cycle_df["spot_price"] = spot_price
    cycle_df["r"] = r
    cycle_df["div_yld"] = div_yld
    all_options_list.append(cycle_df)

if not all_options_list:
    raise ValueError("No options data could be fetched.")

full_df = pd.concat(all_options_list, ignore_index=True)

print(f"Initial raw count: {len(full_df)}")

full_df["rel_spread"] = (full_df["ask"] - full_df["bid"]) / full_df["mid"]

df = full_df.dropna(subset=['bid', 'ask'])
df = df[df['ask'] > 0]

print(f"Count after dropping NaNs and zero asks: {len(df)}")

df = df[
    (df["volume"] > 1) & (df["openInterest"] > 10) 
]

print(f"Count after volume and open interest filter: {len(df)}")


df = df[
    (df["rel_spread"] <= 0.20) & (df["T"] >= 7/365.0) & (df["T"] <= 2.0)
]

df["forward_price"] = df["spot_price"] * np.exp((df["r"] - df["div_yld"]) * df["T"])
df["log_moneyness"] = np.log(df["strike"] / df["forward_price"])

df["tot_variance"] = (df["impliedVolatility"] ** 2) * df["T"]

df = df[
    (df["log_moneyness"] >= -0.30) & (df["log_moneyness"] <= 0.30)
]

df = df[
    ((df["options_type"] == "call") & (df["strike"] >= df["forward_price"])) |
    ((df["options_type"] == "put") & (df["strike"] <= df["forward_price"]))
]

df = df[(df["impliedVolatility"] >= 0.01) & (df["impliedVolatility"] <= 3.0)]

valid_expires = (
    df.groupby("expiration_date")["strike"]
    .count()
    .loc[lambda x: x >= 10]
    .index
)
df = df[df["expiration_date"].isin(valid_expires)]

print(f"Final dataset contains {len(df)} options across {df['expiration_date'].nunique()} expirations.")

script_dir = os.path.dirname(os.path.abspath(__file__))
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = os.path.join(script_dir, f"options_data.csv")

if not df.empty:
    df.to_csv(output_path, index=False)
    print(f"Saved file to: {output_path}")
else:
    print("WARNING: DataFrame is empty after filtering. Try relaxing moneyness or spread filters.")