"""Main entry point for SimpleFin integration."""

from simplefin import SimpleFin, YYYYMMDD_to_epoch
from pprint import pprint
import requests
import os
import pandas as pd
from dotenv import load_dotenv
from simplefin import epoch_to_YYYYMMDD
import matplotlib.pyplot as plt

# CHASE_ACCT_ID = "a37ed0d2-c03a-4af7-99dd-9c9159c67ab9"
CHASE_ACCT_ID = "ACT-a37ed0d2-c03a-4af7-99dd-9c9159c67ab9"
client = SimpleFin()
accounts = client.GetAccounts()

TARGET_BALANCE = 4000

def get_all_accounts():
    print("\nAccounts:")
    print("-" * 60)
    # init empty DataFrame
    accts_df = pd.DataFrame()
    for account in accounts:
        act = pd.json_normalize(account).drop(columns=['transactions'])
        accts_df = pd.concat([accts_df, act], ignore_index=True)
        print(f"{account['name']:30} {account['balance']:>15} {account['currency']} {account['id']}")
    accts_df.to_csv("accounts.csv", index=False)
    print("-" * 60)

def get_chase_transactions():
    response = client.GetAccount(CHASE_ACCT_ID)
    chase_account = response['accounts'][0]
    txns_df = pd.json_normalize(chase_account['transactions'])
    txns_df.to_csv("chase_transactions.csv", index=False)
    return txns_df

def get_chase_balance(date="today"):
    url = f"{os.getenv('ACCESS_URL')}/accounts?account={CHASE_ACCT_ID}&balances-only=true"
    if date != "today":
        date_epoch = YYYYMMDD_to_epoch(date)
        url += f"&balance-date={date_epoch}"
        
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()['accounts'][0]['balance']

def line_graph_over_time(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df['transaction_date'], df['balance'], marker='o')
    plt.xlabel('Date')
    plt.ylabel('Balance')
    plt.title('Balance Over Time')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('balance_chart.png', dpi=100, bbox_inches='tight')
    
def mult_series_plot(df):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Balance line
    ax1.plot(spending_by_day['transaction_date'], spending_by_day['balance'], marker='o', color='blue')
    ax1.set_ylabel('Balance')
    ax1.set_title('Balance Over Time')
    ax1.grid(True)

    # Amount bar chart
    ax2.bar(spending_by_day['transaction_date'], spending_by_day['amount'], color=['red' if x < 0 else 'green' for x in spending_by_day['amount']])
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Amount')
    ax2.set_title('Daily Transactions')
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig('mult_series.png', dpi=100, bbox_inches='tight')

def get_daily_report(date):
    trxs = get_chase_transactions()
    trxs['transaction_date'] = trxs['transacted_at'].apply(epoch_to_YYYYMMDD)
    trxs['amount'] = trxs['amount'].astype(float)
    
    daily_trxs = trxs[trxs['transaction_date'] == date]
    return daily_trxs
    
if __name__ == "__main__":
    load_dotenv()
    
    daily_limit = TARGET_BALANCE / 30
    weekly_limit = TARGET_BALANCE / 4
    
    # get_all_accounts()
    # trxs = get_chase_transactions()
    # trxs['transaction_date'] = trxs['transacted_at'].apply(epoch_to_YYYYMMDD)
    # trxs['amount'] = trxs['amount'].astype(float)

    # balance = -float(get_chase_balance())
    balance = 6195.29
    print("Balance:", balance)
    print("Daily limit:", daily_limit)
    print("Weekly limit:", weekly_limit)

    # spending_by_day = pd.DataFrame(trxs.groupby('transaction_date')['amount'].sum()).reset_index()
    # spending_by_day['report'] = spending_by_day['amount'].apply(lambda x: 'OVER' if -x > daily_limit else 'OK')
    # spending_by_day['avg_L7'] = spending_by_day['amount'].rolling(window=7).sum()
    # spending_by_day = spending_by_day.sort_values('transaction_date', ascending=False)
    # spending_by_day['balance'] = balance + spending_by_day['amount'].cumsum()
    # spending_by_day = spending_by_day.sort_values('transaction_date')
    # spending_by_day.to_csv("spending_by_day.csv", index=False)
    
    spending_by_day = pd.read_csv("spending_by_day.csv")
    
    daily = get_daily_report("20260124").to_csv("daily_report_20260124.csv", index=False)
    
    
    print(spending_by_day.head(30))
    line_graph_over_time(spending_by_day)
    mult_series_plot(spending_by_day)
    
    
    