import subprocess
import re
import datetime
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}

def get_xch_to_usdt():
    url_to_usdt="https://www.gate.io/ja/trade/XCH_USDT"
    request = urllib.request.Request(url_to_usdt, headers=headers)
    res_usdt = urlopen(request)
    soup_usdt = BeautifulSoup(res_usdt, 'html.parser')
    xch_to_usdt = soup_usdt.select("#currPrice")[0].string
    return float(xch_to_usdt)

def get_usd_to_jpy():
    url_to_jpy="https://stocks.finance.yahoo.co.jp/stocks/detail/?code=usdjpy"
    res_jpy = urlopen(url_to_jpy)
    soup_jpy = BeautifulSoup(res_jpy, 'html.parser')
    usd_to_jpy = soup_jpy.select_one(".stoksPrice").string
    return float(usd_to_jpy)


# chia-blockchainのバージョン設定
ver_str = '1.2.9'

# 入金元のプールアドレス
address = [
'xch1address11111111111111111111111111111111111111111111111111111',
'xch1address22222222222222222222222222222222222222222222222222222',
'xch1address33333333333333333333333333333333333333333333333333333',
'xch1address44444444444444444444444444444444444444444444444444444',
'xch1address55555555555555555555555555555555555555555555555555555'
]
xch_count = [0] * len(address)

# 昨日の日付算出
td = datetime.timedelta(days=1)
yesterday = str((datetime.datetime.now()-td).date())

print('Seeking Yesterday\'s amounts')

# chia.exe コマンド実行、戻り値を取得
result = subprocess.getoutput('%APPDATA%/../Local/chia-blockchain/app-'+ver_str+'/resources/app.asar.unpacked/daemon/chia.exe wallet get_transactions --no-paginate')

# 履歴のうち、昨日の取引から各プールアドレスごとに入金量を抽出、加算
lines = result.splitlines() 
xch_total = 0
for i in range(len(lines)):
    m = re.match(r'^Transaction [0-9a-f]{64}$', lines[i])
    if m != None:
        if lines[i+1] == 'Status: Confirmed':
            ma = re.match(r'^Amount.*: (.+) xch$', lines[i+2])
            mw = re.match(r'^To address: (.+)$', lines[i+3])
            md = re.match(r'^Created at: (.+)( [0-9]{2}:[0-9]{2}:[0-9]{2})$', lines[i+4])
            if md.groups()[0] == yesterday:
                for inx, addr in enumerate(address):
                    if address[inx]==mw.groups()[0]:
                        print(md.groups()[0]+md.groups()[1])
                        print(mw.groups()[0])
                        print(ma.groups()[0])
                        xch_count[inx] += float(ma.groups()[0])
                        xch_total += float(ma.groups()[0])
                        break

#XCH/USDT USD/JPY取得
xch_to_usdt = get_xch_to_usdt()
usd_to_jpy = get_usd_to_jpy()
jpy = xch_total * xch_to_usdt * usd_to_jpy
print('xch_total  =', xch_total)
print('xch_to_usdt=', xch_to_usdt)
print('usd_to_jpy =', usd_to_jpy)
print('jpy        =', jpy)

# 抽出結果をcsvに追記
print('Writing csv')

copy_str = yesterday
copy_str += '\t'+'\t'.join(list(map(str,xch_count)))
copy_str += '\t'+str(xch_total)+'\t'+str(xch_to_usdt)+'\t'+str(usd_to_jpy)+'\t'+str(jpy)

with open('chia_wallet_daily_with_jpy.csv', 'a') as f:
    print(copy_str, file=f)


print('Done.')
