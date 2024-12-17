from binance.client import Client
import time

# Binance API anahtarlarını gir
API_KEY = ''
API_SECRET = ''

# Binance istemcisi
client = Client(API_KEY, API_SECRET)

# Binance sunucusu ile sistem zamanını düzelt
def get_time_offset():
    server_time = client.get_server_time()['serverTime']
    local_time = int(time.time() * 1000)
    time_offset = server_time - local_time
    print(f"Zaman farkı: {time_offset} ms")
    return time_offset

# Alım-satım işlemleri
def trade_bot(symbol, buy_price, sell_price, quantity):
    time_offset = get_time_offset()

    while True:
        try:
            # Zaman farkını her istekte uygula
            client._timestamp_offset = time_offset
            
            # Güncel fiyatı al
            ticker = client.get_symbol_ticker(symbol=symbol)
            current_price = float(ticker['price'])
            print(f"Güncel fiyat: {current_price}")

            # Alım işlemi
            if current_price <= buy_price:
                print(f"{symbol} alınacak!")
                order = client.order_market_buy(symbol=symbol, quantity=quantity)
                print(f"Alım yapıldı: {order}")
            
            # Satım işlemi
            elif current_price >= sell_price:
                print(f"{symbol} satılacak!")
                order = client.order_market_sell(symbol=symbol, quantity=quantity)
                print(f"Satım yapıldı: {order}")

            time.sleep(5)  # 5 saniye bekle
        except Exception as e:
            print(f"Hata: {e}")
            time.sleep(5)

# Kullanıcı girdileri
symbol = "BTCUSDT"      # İşlem çifti
buy_price = 30000       # Alım fiyatı
sell_price = 32000      # Satım fiyatı
quantity = 0.001        # İşlem miktarı (örnek: 0.001 BTC)

# Botu başlat
trade_bot(symbol, buy_price, sell_price, quantity)
