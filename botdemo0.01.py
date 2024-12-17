 

pip install python-binance

from binance.client import Client
import time

# Binance API Anahtarlarınız
API_KEY = 'your_api_key_here'
API_SECRET = 'your_api_secret_here'

# Binance Client'ı başlat
client = Client(API_KEY, API_SECRET)

# İşlem yapacağınız kripto parayı seçin
symbol = 'BTCUSDT'  # Bitcoin/USDT çifti
quantity = 0.001    # Alım/Satım yapılacak miktar

# Basit bir strateji: Fiyat belirli bir seviyenin altına düşerse al, yukarı çıkarsa sat
BUY_THRESHOLD = 17000  # Alım fiyat seviyesi
SELL_THRESHOLD = 18000 # Satış fiyat seviyesi

def get_price(symbol):
    """Anlık fiyatı al."""
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def buy(symbol, quantity):
    """Piyasadan alım yap."""
    order = client.order_market_buy(
        symbol=symbol,
        quantity=quantity
    )
    print(f"Alım yapıldı: {order}")
    return order

def sell(symbol, quantity):
    """Piyasadan satış yap."""
    order = client.order_market_sell(
        symbol=symbol,
        quantity=quantity
    )
    print(f"Satış yapıldı: {order}")
    return order

def main():
    """Ana döngü."""
    while True:
        try:
            price = get_price(symbol)
            print(f"Güncel Fiyat: {price}")

            if price < BUY_THRESHOLD:
                print(f"Fiyat {BUY_THRESHOLD}'nin altında! Alım yapılıyor...")
                buy(symbol, quantity)

            elif price > SELL_THRESHOLD:
                print(f"Fiyat {SELL_THRESHOLD}'nin üstünde! Satış yapılıyor...")
                sell(symbol, quantity)

            # Döngüdeki bekleme süresi (15 saniye)
            time.sleep(15)

        except Exception as e:
            print(f"Hata: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()
