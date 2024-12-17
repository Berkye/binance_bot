import ccxt
import pandas as pd
from time import sleep

API_KEY = ""
API_SECRET = ""

# ccxt ile Spot Testnet bağlantısı
# urls.api içindeki 'public' ve 'private' değerlerini testnet endpoint'ine yönlendiriyoruz.
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'spot',  # Spot işlemler için
    },
    'urls': {
        'api': {
            'public': 'https://testnet.binance.vision/api',
            'private': 'https://testnet.binance.vision/api',
        }
    }
})

symbol = "BTC/USDT"

def main():
    try:
        # 1) Bakiye Çekme
        balance = exchange.fetch_balance()
        print("Bakiyeler:", balance)

        # 2) Piyasa Verisi Çekme (Örnek: OHLCV)
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=5)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        print("\nSon 5 mum verisi:\n", df)

        # 3) Limit Alış Emri Gönderme (örnek)
        # Gerçek parayla işlem yapmıyorsunuz, testnet'tesiniz. Yine de dikkatli test edin.
        order_price = 10000  # BTC/USDT hypotetik düşük bir fiyat: ~10,000 USDT
        amount = 0.001       # 0.001 BTC alım emri
        print("\nLimit Alış Emri Gönderiliyor... (BTC/USDT, Price={}, Amount={})".format(order_price, amount))
        order = exchange.create_limit_buy_order(symbol, amount, order_price)
        print("Gönderilen Emir:", order)

        # 4) Açık Emirleri Listeleme
        open_orders = exchange.fetch_open_orders(symbol)
        print("\nAçık Emirler:", open_orders)

        # 5) Bir süre bekleyip deneme amaçlı iptal edebilirsiniz
        sleep(5)
        if open_orders:
            order_id = open_orders[0]['id']
            cancel = exchange.cancel_order(order_id, symbol)
            print("\nEmir İptal Edildi:", cancel)

    except ccxt.BaseError as e:
        print("Hata oluştu:", e)

if __name__ == "__main__":
    main()
