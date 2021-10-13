# Get_Chia_DailyIncome
## Chiaの毎日の収入を取得するスクリプト

Chia BlockchainがインストールされたPCで、  
`chia.exe wallet get_transactions` の出力を利用して、  
昨日の入金データを集計するスクリプト


## 事前準備
get_chia_income.py を開き、以下の2つの設定を行ってください  
1. ver_str = '1.2.9' を自身のchia-blockchainのバージョンに合わせる  
2. address 中の  
xch1address11111111111111111111111111111111111111111111111111111  
以下のアドレスを、参加中のプールの「支払先アドレス」に置き換える  
(PoolタブのYour Pool Overviewで参加中プールのアドレスを確認、コピペしておいて下さい)  

## 実行方法

`python get_chia_income.py`

→ chia_wallet_daily.csv に、昨日の入金データが追記されます。  
これを、毎日定時に1回タスクスケジューラなどで実施することで、  
毎日の自動記帳を行うことができます。
