# ファイル構成

* `solver`: kurenaifが検証に使ったファイルが雑に置かれています
* `witchquiz`: サーバ本体です(django)
    * `problemFiles`: 配布しているファイルです
    * `witchquiz/datas`: 問題の時間設定、ユーザ名やトークンの設定ができます

# 遊び方

1. `/witchquiz/witchquiz/datas/problems.json` のstarttimeを設定します。starttimeは 1時間、2時間、2時間、2時間の間隔で設定すると本番のものと同じになります。
    * tickcountはそのラウンドのtickの個数
    * tickintervalは1tickあたりの秒数です。
    * starttimeを同時にスタートさせると、同時開催することが可能です（APIは動作しますが、スコアボードがバグるのでデバッグ用です）
2. `bash initialdb_setup.bash` を叩きます。これを叩くことでサーバの起動とDBの初期化が行われます。
3. `localhost` にアクセスします
4. `token1` でログインします

# Q&A

[kurenaifに聞いてください](https://twitter.com/fwarashi)