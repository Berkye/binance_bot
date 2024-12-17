import time
import base64
import requests
from binance.client import Client
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# Binance API anahtarları
API_KEY = '  # Buraya kendi API Key'inizi yazın
API_SECRET = '  # Buraya kendi Secret Key'inizi yazın
PRIVATE_KEY_PATH = 'test-prv-key.pem'  # Özel anahtar dosyanızın yolu

# Binance istemcisi (Testnet için endpoint belirtilir)
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'  # Spot Testnet URL

# Özel anahtarı yükle
def load_private_key():
    with open(PRIVATE_KEY_PATH, 'rb') as f:
        private_key = load_pem_private_key(data=f.read(), password=None)
    return private_key

# API için zaman damgası oluştur ve imzala
def sign_request(params, private_key):
    # Zaman damgası ekle
    timestamp = int(time.time() * 1000)
    params['timestamp'] = timestamp

    # İmza oluştur
    payload = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = base64.b64encode(private_key.sign(payload.encode('ASCII')))
    params['signature'] = signature
    return params

# Limit emir gönderme
def send_limit_order(symbol, side, quantity, price):
    private_key = load_private_key()

    # Parametreleri ayarla
    params = {
        'symbol': symbol,
        'side': side,  # "BUY" veya "SELL"
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': quantity,
        'price': price,
    }

    # İmzalı istek
    signed_params = sign_request(params, private_key)

    # API isteğini gönder
    headers = {'X-MBX-APIKEY': API_KEY}
    response = requests.post(
        f"{client.API_URL}/v3/order",
        headers=headers,
        data=signed_params
    )
    return response.json()

# Alım-satım botu
def trade_bot(symbol, buy_price, sell_price, quantity):
    while True:
        try:
            # Güncel fiyatı al
            ticker = client.get_symbol_ticker(symbol=symbol)
            current_price = float(ticker['price'])
            print(f"Güncel fiyat: {current_price} USDT")

            # Alım işlemi (Limit emir)
            if current_price <= buy_price:
                print(f"{symbol} alınacak! Limit emir gönderiliyor...")
                order = send_limit_order(symbol, 'BUY', quantity, buy_price)
                print(f"Limit alım emri gönderildi: {order}")

            # Satım işlemi (Limit emir)
            elif current_price >= sell_price:
                print(f"{symbol} satılacak! Limit emir gönderiliyor...")
                order = send_limit_order(symbol, 'SELL', quantity, sell_price)
                print(f"Limit satım emri gönderildi: {order}")

            time.sleep(5)  # 5 saniye bekle
        except Exception as e:
            print(f"Hata: {e}")
            time.sleep(5)

# Kullanıcı girdileri
symbol = "BTCUSDT"      # İşlem çifti (örnek: BTC/USDT)
buy_price = 30000       # Alım yapılacak fiyat (USDT)
sell_price = 32000      # Satış yapılacak fiyat (USDT)
quantity = 0.001        # İşlem miktarı (örnek: 0.001 BTC)

# Botu başlat
trade_bot(symbol, buy_price, sell_price, quantity)
