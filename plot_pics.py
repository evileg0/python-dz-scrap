import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

conn = sqlite3.connect('moex_db.db')

query = "SELECT * FROM stocks;"
df = pd.read_sql(query, conn)

# Переводим в формат datetime
df['time'] = pd.to_datetime(df['time'])

if df.empty:
    print("База данных пуста.")
    exit()

# Получаем список уникальных тикеров с именами
unique_tickers = df.groupby('ticker')['name'].first().to_dict()

output_dir = "pics"
if os.path.exists(output_dir):
    for filename in os.listdir(output_dir):
        if filename.endswith('.png'):
            file_path = os.path.join(output_dir, filename)
            os.remove(file_path)
os.makedirs(output_dir, exist_ok=True)


for ticker, name in unique_tickers.items():
    ticker_data = df[df['ticker'] == ticker][['time', 'price']]
    ticker_name = df

    if ticker_data.empty:
        print(f"Нет данных для тикера {ticker}.")
        continue

    ticker_data = ticker_data.sort_values(by='time')

    plt.figure(figsize=(12, 8))
    plt.plot(ticker_data['time'], ticker_data['price'], marker='o', label=f"{ticker} цена")
    plt.title(f"Изменение цены для {name} {ticker}")
    plt.xlabel("Время")
    plt.ylabel("Цена")
    plt.grid(True)
    plt.legend()

    plot_filename = os.path.join(output_dir, f"{ticker}_price_change.png")
    plt.savefig(plot_filename)
    print(f"График для {ticker} сохранён {plot_filename}")

    plt.clf()

conn.close()