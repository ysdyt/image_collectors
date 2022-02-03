# image_collectors
画像検索APIを叩いて画像収集するやつです（スクレイピングではなく、正規の手順でAPIを叩きます）  
BingとGoogleそれぞれのパターンがありますので、所属する宗教の方をお使いください。救われさえすればいいという無宗教の方はBingを強くおすすめします。

スクレイピングではなくAPIを使うため課金が発生しますが、アカウント設立時に貰える無料クーポンで実質無料みたいなもんです（クーポン利用期間制限はありますが）

それぞれの詳細は以下もご参照ください

- [Bingの画像検索APIを使って画像を大量に収集する - Qiita](https://qiita.com/ysdyt/items/49e99416079546b65dfc)
- [Googleの画像検索APIを使って画像を大量に収集する - Qiita](https://qiita.com/ysdyt/items/02a9e6b4e70f26385abc)

## 実行環境
- Python3

## 実行方法

### API keyの設定

Bing or GoogleのAPI keyを事前に取得している前提です。  
API keyは実行スクリプトとは別のファイル`authentication.ini`に書き込み、`configparse`で読み出す形式になっています。

まず、`bing_image_collector.py`などがあるのと同じ階層で`authentication.ini`ファイルを作成します。

```bash
$ touch authentication.ini
```
作成した`authentication.ini`に取得したAPI keyを以下のように書き込みます。BingとGoogleで必要なkeyだけ書けば大丈夫です（両方は必要ありません）。

```text
[auth]
bing_api_key = xxxxxxxxxxxxxxxx
google_api_key = xxxxxxxxxxxxxxxxx
google_se_key = xxxxxxxxxxxxx
```
（注意！）文字列はシングルコートなどで囲わずそのまま書き込む

- `bing_api_key` ・・・ Bing Image Search APIのkeyを指定します。API keyの取得方法の例は[こちら](https://qiita.com/ysdyt/items/49e99416079546b65dfc)
- `google_api_key` ・・・ Google Custom Search APIのkeyを指定します。API keyの取得方法の例は[こちら](https://qiita.com/ysdyt/items/02a9e6b4e70f26385abc)
- `google_se_key` ・・・ Google Custom Engineのkeyを指定します。Google Custom Search APIを利用するには Search API用のkeyの他に、Custom Engineのkeyも必須となります。取得例は[こちら](https://qiita.com/onlyzs/items/c56fb76ce43e45c12339)



### スクリプトの実行

**Bing Image Search APIを利用する場合**

```bash
$ python3 bing_image_collector.py
```
検索クエリーやパラメータなどの指定方法は[Qiita](https://qiita.com/ysdyt/items/49e99416079546b65dfc)にまとめました

**Google Custom Search APIを利用する場合**

```bash
$ python3 google_image_collector.py
```
検索クエリーやパラメータなどの指定方法は[Qiita](https://qiita.com/ysdyt/items/02a9e6b4e70f26385abc)にまとめました
