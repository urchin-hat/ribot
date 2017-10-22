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
`やります` or `ごめんなさい`に分類する  
↓  
`やります`に移動した場合にissueを作る  
↓  
作業着手    
↓  
実装したら`できました`に移動

コミットは1.実装内容 2.helpの文言、README.mdの更新 の2つぐらいが理想

## コマンド
コマンドの一覧と簡単な説明
チャンネル内なら`@ribot ヘルプ` or `@ribot help`、1on1であれば`ヘルプ` or `help`と呟くとヘルプを表示します。

---
### メンションが必要なもの(1on1なら不要です)
#### 完全一致じゃないと反応しないもの
##### 1. Hello World
> _`@ribot はろー`_

と呟くと動作します。
##### 2. 天気
ライブドア天気情報apiを使用してます。  
http://weather.livedoor.com/weather_hacks/webservice
> _`@ribot {都市名}の天気`_

と呟くと天気情報を返してくれます。
都市名がない場合はエラーを返します。その場合は[地域ID](http://weather.livedoor.com/forecast/rss/primary_area.xml)を参考にしてください。
##### 3. BTCレート
bitFlyer APIより取得してます。  
https://bitflyer.jp/ja/api
> _`@ribot BTCのレート`_

と呟くとBTCの売値買値を返します。
#### 引数が必要なもの
##### 1. ウィキペディア検索
> _`@ribot wiki {調べたいこと}`_

でwikipediaの`https://ja.wikipedia.org/wiki/{調べたいこと}`のURLを返します。存在しなければエラーを返します。
##### 2. Linuxコマンド検索
以下のサイトからスクレイピングをしています。
http://www.k4.dion.ne.jp/~mms/unix/linux_com/

> _`@ribot コマンド {コマンド名}`_

でLinuxコマンドの機能と書式を返します。

---
### メンションじゃなくても拾ってくれるもの(チャンネル限定)
#### 完全一致じゃないと反応しないもの
##### 1. お疲れ様
> _`お疲れ様です`_

と呟くと動作動作します。
#### 引数がいるもの
##### 1. ランダム選出
> _`選出 ○人`_

と呟くとチャンネル内からランダムで選出します。　
##### 2. 簡易アンケート
> _`アンケート お題 項目1 項目2...`_

と呟くとアンケートを作成します。
##### 3. トピック設定
> _`トピック 設定するトピック`_

と呟くとトピックを設定します。

### どっちでも反応してくれるもの
#### 完全一致じゃないと反応しないもの
##### 1. 書籍情報
> _`新書 or 書籍 or 新刊`_

または
>_`@ribot 新書 or @ribot 書籍 or @ribot 新刊`_

と呟くとオライリーの新書情報を返します。
##### 2. ニュース
> _`ニュース`_

または
> _`@ribot ニュース`_

と呟くとスラドの最新5件のニュースを返します。

#### 両方反応するもの
##### 1. おにぎり
>_`@ribot おにぎり`_

または
>_`今日のおにぎり`_

でおにぎりをオススメのおにぎりを教えてくれる。
### デフォルト返信
A3RTを使用  
https://a3rt.recruit-tech.co.jp/  
A3RTのTalk APIで塩対応してくれるよー

---
### admin機能
**！！！この関数の説明はヘルプに乗っていないです(管理用機能)！！！**
#### 1. コマンド実行
>`@ribot ribot_root {command}`

で実行サーバー内のコマンド結果を返します(1on1でやるのが望ましい)
