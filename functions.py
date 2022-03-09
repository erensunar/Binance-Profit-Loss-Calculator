

from binance import Client
apiKey = ""
apiSecret = ""
client = Client(apiKey, apiSecret)



def getWallet():
    account = client.get_account()["balances"]
    print(account)
    for i in account:
        if float(i["free"]) > 0.0:
            pass

def filter(symbol):
    parities = ["BUSD", "USDT", "BTC", "BNB"]
    for i in parities:
        location = symbol.find(i)
        if location > 0:
            return symbol[:location]


#Spot cüzdanda ilgili sembolün miktarı
def getQty(symbol):

    symbol = filter(symbol)

    account = client.get_account()["balances"]
    for i in account:
        if float(i["free"]) > 0.0 and i["asset"] == symbol:
            return i["free"]
        
    return 0


#İlgili sembolün satın alma geçmişi
def getBuyHistory(symbol):
    history= []
    log = client.get_my_trades(symbol = symbol)
    for i in log:
        if i["isBuyer"] :
            history.append({"price": i["price"], "qty": i["qty"]})
    return history


#İlgili sembolün satış geçmişi
def getSellHistory(symbol):
    history= []
    log = client.get_my_trades(symbol = symbol)
    for i in log:
        if not i["isBuyer"]:
            history.append({"price": i["price"], "qty": i["qty"]})
           
    return history

#Tüm zamanlara göre kar/zarar miktarı
def profitHistory(symbol):
    buyLog = getBuyHistory(symbol)
    sellLog = getSellHistory(symbol)
    currencyValue = getCurrentValue(symbol)

    buy = 0
    for i in buyLog:
        buy += float(i["price"]) *  float(i["qty"])
    buy -= currencyValue
    sell = 0
    for i in sellLog:
        sell += float(i["price"]) *  float(i["qty"])
    if sell - buy > 0:
        print("Profit: ", sell - buy )
    elif buy - sell == 0:
        print("Profit: 0")
    else:
        print("Loss: ", (buy - sell))

#Coinin anlık fiyatı
def getPrice(symbol):
    info = client.get_symbol_ticker(symbol=symbol)
    return  info["price"]


#Coinin cüzdandaki değeri
def getCurrentValue(symbol):
    qty = getQty(symbol)
    price = getPrice(symbol)
    return float(qty) * float(price)


