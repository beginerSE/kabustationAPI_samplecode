import urllib.request
import pprint
import json

host_ = '18080'
pass_ = '*****'

def generate_token():
    obj = {'APIPassword': pass_}
    json_data = json.dumps(obj).encode('utf8')
    url = f'http://localhost:{host_}/kabusapi/token'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as res:
            content = json.loads(res.read())    
            token_value = content.get('Token')
    except urllib.error.HTTPError as e:
        print(e)
    return token_value


# 銘柄情報を取得
def get_symbol(market, code, token):
    url_symbol = f'http://localhost:{host_}/kabusapi/symbol/{code}@{market}'
    req_symbol = urllib.request.Request(url_symbol, method='GET')   
    req_symbol.add_header('X-API-KEY', token)
    try:
        with urllib.request.urlopen(req_symbol) as res_symbol:
            content_symbol = json.loads(res_symbol.read())
    except urllib.error.HTTPError as e_symbol:
        print(e_symbol)
        content_symbol = json.loads(e_symbol.read())
    return content_symbol


#注文一覧を取得
def get_order(token,order_type=0):
    url = f'http://localhost:18080/kabusapi/orders?product={order_type}'
    response = requests.get(url, headers={'X-API-KEY': token,})
    orders = json.loads(response.text)
    data = []
    for order in orders:
#         print(order)
        state = order['State']
        if state >= 4:  # 1,2,3: 待機,処理中,処理済
            continue

        price = order['Price']
        if price == 0.0:
            price = '成行  '

        side = order['Side']
        if side == '2':
            side = '買'
        elif side == '1':
            side = '売'

        board = get_priceinfo(1, order['Symbol'], token)
        current_price = board["CurrentPrice"]
        if current_price == None:
            current_price = "---"

        data.append(
            [order['ID'],
             order['Symbol'],
             order['SymbolName'],
             price,
             side,
             order['OrderQty'],
             current_price,
             order['ExpireDay'],
            ])

    return pd.DataFrame(data, columns=['注文ID','コード','銘柄', '注文価格','売/買','注文数','現在価格','期限'])

# ポジション一覧(現物・信用)を取得する関数
def get_position(token, product=0):
    url = f'http://localhost:18080/kabusapi/positions?product={product}'
    response = requests.get(url, headers={'X-API-KEY': token,})
    positions = json.loads(response.text)
    data = []
    for position in positions:
        print(position)
        if position['Side'] == '2':
            side='買'
        elif position['Side'] == '1':
            side = '売'
        try:
            typeid = position['MarginTradeType']
            ordertype = '信用'
        except:
            typeid = -1
            ordertype = '現物'
        data.append(
                [ordertype,
                 typeid,
                 position['ExecutionID'],
                 position['Symbol'],
                 position['SymbolName'],
                 side,
                 position['Price'],
                 position['LeavesQty'],
                 position['CurrentPrice'],
                 position['ProfitLoss']]
            )
    
    return pd.DataFrame(data, columns=['注文種別','信用注文タイプ','ポジションID','コード','銘柄', '売買','注文価格','注文数','現在価格', '損益'])

# 現物余力を取得する関数
def get_cashbalance(token,symbol=None):
    #symbol: 現物の各銘柄の保有枚数
    if symbol == None:
        url = f'http://localhost:18080/kabusapi/wallet/cash'
        response = requests.get(url, headers={'X-API-KEY': token,})
        cash = json.loads(response.text)
        return cash['StockAccountWallet']
    else:
        url = f'http://localhost:18080/kabusapi/wallet/cash/{symbol}'
        print(url)
        response = requests.get(url, headers={'X-API-KEY': token,})
        cash = json.loads(response.text)
        return cash
    

# 信用余力を取得する関数
def get_marginbalance(token,symbol=None):
    #symbol: 現物の各銘柄の保有枚数

    if symbol == None:
        url = f'http://localhost:18080/kabusapi/wallet/margin'
    else:
        url = f'http://localhost:18080/kabusapi/wallet/margin/{symbol}'
    response = requests.get(url, headers={'X-API-KEY': token,})
    cash = json.loads(response.text)
#     print(cash)
    return cash
