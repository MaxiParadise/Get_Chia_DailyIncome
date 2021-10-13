import subprocess
import re
import datetime

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
for i in range(len(lines)):
    m = re.match(r'^Transaction [0-9a-f]{64}$', lines[i])
    if m != None:
        if lines[i+1] == 'Status: Confirmed':
            ma = re.match(r'^Amount: (.+) xch$', lines[i+2])
            mw = re.match(r'^To address: (.+)$', lines[i+3])
            md = re.match(r'^Created at: (.+)( [0-9]{2}:[0-9]{2}:[0-9]{2})$', lines[i+4])
            if md.groups()[0] == yesterday:
                xch_total = 0
                for inx, addr in enumerate(address):
                    if address[inx]==mw.groups()[0]:
                        print(md.groups()[0]+md.groups()[1])
                        print(mw.groups()[0])
                        print(ma.groups()[0])
                        xch_count[inx] += float(ma.groups()[0])
                        xch_total += float(ma.groups()[0])
                        break

# 抽出結果をcsvに追記
print('Writing csv')

copy_str = yesterday
copy_str += '\t'+'\t'.join(list(map(str,xch_count)))
copy_str += '\t'+str(xch_total)

with open('chia_wallet_daily.csv', 'a') as f:
    print(copy_str, file=f)


print('Done.')
