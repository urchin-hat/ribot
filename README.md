# ribot
社内slackbot
## 実行環境
```bash
$ python -V
Python 3.6.0 :: Anaconda 4.3.0 (x86_64)
```
`Python 3.6`環境らしいです。

## 使用パッケージ
- slackbot - https://github.com/lins05/slackbot  
- Beautiful Soup - https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- pya3rt - https://github.com/nocotan/pya3rt
- feedparser - https://github.com/kurtmckee/feedparser

## 実装の心構え
[カンバン](https://github.com/urchin-hat/ribot/projects/1)に要望を上げる。  
↓  
やります or ごめんなさいに分類する  
↓  
やりますに移動した場合にissueを作る  
↓  
作業着手    
↓  
実装したらできましたに移動

コミットは1.実装内容 2.helpの文言、README.mdの更新 の2つぐらいが理想

## コマンド
コマンドの一覧と簡単な説明
`ヘルプ` or `help`と呟くとコマンドの一覧が出ます。

### 天気
ライブドア天気情報apiを使用  
http://weather.livedoor.com/weather_hacks/webservice
```
{都市名}の天気
```
と呟くと天気情報を返します。

### 書籍
スクレイピング対象はオライリー公式サイト  
https://www.oreilly.co.jp/index.shtml
```
新刊 or 書籍 or 新書
```
と呟くと書籍情報を返します。

### ニュース
スラドから取得  
https://srad.jp/
```
ニュース
```
と呟けば新着のニュース5件を返します。

### ランダム選出
```
選出 ○○人
```
と呟けばランダムで選出してくれます。ただプライベートなチャンネルは非対応です。

### アンケート
```
アンケート 項目1 項目2 …
```
と呟くと簡易的なアンケートを作成します。

### BTC
bitFlyer APIより取得  
https://bitflyer.jp/ja/api
```
BTCのレート
```
と呟くと売値と買値教えてくれるよ。

### おにぎり
```
おにぎり
```
と呟けばオススメのおにぎりを返してくれるかも。
