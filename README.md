# image_collectors
BingやGoogleのAPIを叩いて画像収集するやつ

## 実行環境
- Python3

## 実行方法

### API keyの設定

API keyなどは実行スクリプトとは別に作るファイル（authentication.ini）に書き込み、`configparse`で読み出す形式になっている。

bing_image_collector.pyなどがあるのと同じ階層で

```bash
$ touch authentication.ini
```
authentication.iniの中に別途取得したAPI keyを以下のように書き込む

```text
[auth]
bing_api_key = a0fc89cbhoge4eb2hogeabhoge98dfa9173
google_api_key = AIzahyBrhogewXWs6GglVfQmisdfaghN4-Wgffspw
google_se_key = 00345296485734547770:cfjdifgq18-c
```
（注意！）文字列はシングルコートなどで囲わずそのまま書き込む

### スクリプトの実行

