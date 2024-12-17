import time
import pandas as pd
import numpy as np
from datetime import datetime
from binance.client import Client
from binance.enums import *
import traceback
    

# ------------------------------------------------------
# Lütfen kendi SPOT TESTNET API KEY ve SECRET'ınızı girin
API_KEY = ""
API_SECRET = ""
# ------------------------------------------------------

# Python-Binance ile Spot Testnet'e bağlanmak için:
client = Client(API_KEY, API_SECRET, testnet=True)

# Bot Parametreleri
SYMBOL = 'BTCUSDT'     # İşlem çifti (Spot Testnet'te BTCUSDT genelde mevcut)
INTERVAL = '1m'        # Mum aralığı: '1m', '5m', '15m', '1h', vb.
LIMIT_CANDLES = 100    # Geçmiş veri çekmek için mum sayısı
QTY = 0.001            # Alınacak/satılacak BTC miktarı
RSI_PERIOD = 14        # RSI hesaplamak için kullanılan mum sayısı
RSI_LOWER = 30         # RSI bu eşiğin altına inerse AL sinyali
RSI_UPPER = 70         # RSI bu eşiğin üstüne çıkarsa SAT sinyali

def calculate_RSI(df, period=14):
    """
    Verilen 'close' sütununa göre RSI (Relative Strength Index) değerlerini hesaplar.
    df: 'close' sütunu içeren bir pandas DataFrame
    period: RSI hesaplamasında kullanılacak mum sayısı (14 yaygın bir değerdir)
    """
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).ewm(alpha=1/period).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_historical_klines(symbol, interval, limit=100):
    """
    Spot Testnet'ten 'symbol' için belirli 'interval' aralığındaki en son 'limit' mum verisini çeker.
    Geriye pandas DataFrame döndürür.
    """
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, 
                      columns=['open_time', 'open', 'high', 'low', 'close', 'volume',
                               'close_time', 'quote_av', 'trades', 'tb_base_av', 
                               'tb_quote_av', 'ignore'])
    
    # Sütunları numerik tipe dönüştür
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low']  = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)

    return df

def place_buy_order(symbol, quantity):
    """
    Belirli bir coin çiftine (symbol) ve miktara (quantity) göre
    piyasa (market) alış emri gönderir.
    """
    try:
        print(f"[BUY] Market alış emri gönderiliyor... {symbol}, miktar: {quantity}")
        order = client.create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print("Alış emri başarıyla gerçekleşti:", order)
        return order
    except Exception as e:
        print("Alış emri hatası:", e)
        traceback.print_exc()
        return None

def place_sell_order(symbol, quantity):
    """
    Belirli bir coin çiftine (symbol) ve miktara (quantity) göre
    piyasa (market) satış emri gönderir.
    """
    try:
        print(f"[SELL] Market satış emri gönderiliyor... {symbol}, miktar: {quantity}")
        order = client.create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print("Satış emri başarıyla gerçekleşti:", order)
        return order
    except Exception as e:
        print("Satış emri hatası:", e)
        traceback.print_exc()
        return None

def run_trading_bot():
    """
    Basit RSI stratejisi: RSI_LOWER altındayken market alış, RSI_UPPER üzerindeyken market satış.
    in_position: Elimizde BTC var mı? Basit bir durum takibi için kullanılır.
    """
    in_position = False

    while True:
        try:
            df = get_historical_klines(SYMBOL, INTERVAL, LIMIT_CANDLES)
            df['rsi'] = calculate_RSI(df, period=RSI_PERIOD)
            current_rsi = df['rsi'].iloc[-1]  # En güncel RSI değeri
            
            current_price = df['close'].iloc[-1]
            print(f"[{datetime.now()}] {SYMBOL} Fiyat: {current_price:.2f}, RSI: {current_rsi:.2f}")

            # RSI değerine göre al/sat kararı
            if current_rsi <= RSI_LOWER and not in_position:
                # AL
                order = place_buy_order(SYMBOL, QTY)
                if order is not None:
                    in_position = True

            elif current_rsi >= RSI_UPPER and in_position:
                # SAT
                order = place_sell_order(SYMBOL, QTY)
                if order is not None:
                    in_position = False

            # 15 saniyede bir tekrar kontrol
            time.sleep(15)

        except Exception as e:
            print("Bot çalışırken bir hata oluştu:", e)
            traceback.print_exc()
            time.sleep(15)

if __name__ == "__main__":
    run_trading_bot()
