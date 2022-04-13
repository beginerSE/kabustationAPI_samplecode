
# 現物注文を出す関数
def send_cashorder(token, pass_, symbol, exchange, side, ordertype, qty, price, expire):
    
    if side == 'buy':
        side = '2'
        dtype = 2
        ftype = 'AA'
    elif side == 'sell':
        side = '1'
        dtype = 0
        ftype = '  '
    # 成行注文のときのオプション
    if str(ordertype) == '10':  
        price = 0
    obj = { 'Password': pass_,
            'Symbol': str(symbol),       # 銘柄コード
            'Exchange': int(exchange),          #1が「東証」
            'SecurityType': 1,      # 1が「株式」
            'Side': side,            # 1が「売り」、2が「買い」
            'CashMargin': 1,  #1が「現物」 2が「信用新規」 3が「信用返済」
            'DelivType': dtype,  # 1が「制度信用」 2が「長期」 3が「デイトレ」
            'AccountType': 2, # 口座の種類　2が「一般」
            'Qty': int(qty),
            'FrontOrderType': int(ordertype),
            'FundType':ftype,
            'Price': price,
            'ExpireDay': expire
              }
    #print(obj)
    json_data = json.dumps(obj).encode('utf-8')

    url = 'http://localhost:18080/kabusapi/sendorder'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', token)

    try:
        with urllib.request.urlopen(req) as res:
            #print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            content = json.loads(res.read())
            return content
    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        return content
    except Exception as e:
        return e

# 注文を取り消す関数
def cancel_order(token, pass_, id_):
    url = 'http://localhost:18080/kabusapi/cancelorder'
    obj = {
        'Password': pass_,
        'OrderId': id_
    }
    json_data = json.dumps(obj).encode('utf-8')
    req = urllib.request.Request(url, json_data, method='PUT')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', token)

    try:
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            content = json.loads(res.read())
#             pprint.pprint(content)
            return content
    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
#         pprint.pprint(content)
        return content
    except Exception as e:
#         print(e)
        return e

# 信用取引の注文を出す関数
def send_marginorder(token, pass_, symbol, exchange, side, margintype, ordertype,qty, price, expire):
    
    if side == 'buy':
        side = '2'
    elif side == 'sell':
        side = '1'
    if int(ordertype) == 10:
        price = 0
    obj = { 'Password': pass_,
            'Symbol': str(symbol),       # 銘柄コード
            'Exchange': int(exchange),          #1が「東証」
            'SecurityType': 1,      # 1が「株式」
            'Side': side,            # 1が「売り」、2が「買い」
            'CashMargin': 2,  #1が「現物」 2が「信用新規」 3が「信用返済」
            'MarginTradeType': margintype, 
            'DelivType': 0,
            'AccountType': 2, # 口座の種類　2が「一般」
            'Qty': int(qty),
            'FrontOrderType': ordertype,
            'Price': price,
            'ExpireDay': expire
          }

        
    print(obj)
    json_data = json.dumps(obj).encode('utf-8')

    url = 'http://localhost:18080/kabusapi/sendorder'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', token)

    try:
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            content = json.loads(res.read())
            return content
    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
#         pprint.pprint(content)
        return content
    except Exception as e:
#         print(e)
        return e

# ポジションを決済する関数
def send_margin_closeorder(token, pass_, exchange, order_id, order_type, price, expire):
    position_data = get_position(token,2)
    posi_data = position_data[position_data['ポジションID']==order_id]
    qty = posi_data['注文数'][0]
#     print('ggu',side)
    if order_type == 10:
        price = 0
    if posi_data['売買'][0]=='買':
        print(1)
        side = '1'
    elif posi_data['売買'][0]=='売':
        print(2)
        side = '2'
    margintype = posi_data['信用注文タイプ'][0]
    symbol = posi_data['コード'][0]
    obj = { 'Password': pass_,
            'Symbol': str(symbol),       # 銘柄コード
            'Exchange': int(exchange),          #1が「東証」
            'SecurityType': 1,      # 1が「株式」
            'FrontOrderType': order_type,
            'TimeInForce': 0,
            'Side': side,            # 1が「売り」、2が「買い」
            'CashMargin': 3,  #1が「現物」 2が「信用新規」 3が「信用返済」
            'MarginTradeType': int(margintype), 
            'DelivType': 2,
            'FundType': 11,
            'AccountType': 2, # 口座の種類　2が「一般」
            'Qty': int(qty),
            'Price': int(price),
            'ExpireDay': expire,
            'ClosePositions': [{'HoldID':order_id ,'Qty':int(qty)}]
          }

    print(obj)
    json_data = json.dumps(obj).encode('utf-8')

    url = 'http://localhost:18080/kabusapi/sendorder'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', token)

    try:
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            content = json.loads(res.read())
            return content
    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
#         pprint.pprint(content)
        return content
    except Exception as e:
#         print(e)
        return e
