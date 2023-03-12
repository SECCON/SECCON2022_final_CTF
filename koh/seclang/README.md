# SecLang

## 構成

`distfiles`に配布ファイルがある。

`challenges`にサーバー側のファイルがある。

- `docs`: 言語仕様
- `engine/compiler`: コンパイラ
- `engine/assembler`: アセンブラ
- `engine/executor`: 実行環境
- `engine/interpreter`: インタプリタ
- `engine/sample`: サンプルプログラム
- `server`: サーバー
- `worker`: ワーカー（各種要求の受付）
- `testcase`: テストケース一覧
- `simulator`: シミュレータ

## デプロイ

黒魔術

### エンジンの整備
`engine`で`01_build_docker.sh`を動かし、実行・コンパイル環境を整備する。
また、`engine/interpreter`で`docker-compose up -d`してインタプリタを動作させる。

サンプルプログラムを`02_compile.sh`でコンパイルし、`03_execute.sh`で実行できたら成功。

### redisの起動

```
# apt install redis-server
$ pip install redis
```

Redisサーバーを起動しておく。

### サーバーの起動

```
$ pip install Flask
```

`server/config.json`を適当に変更し、`app.py`を実行する。
本番ではnginxとuwsgiを適当に設定し、`server/uwsgi.ini`を直して動かす。

`server/prepare_container.py`を動かすと、全チームのコンテナを初期状態に設定できる。
また、`gen_report.py`を動かして、攻撃ログを削除する。
最後にパスワード（チームトークン）を適当に変更し、`gen_testcase.py`でデータベースを初期化する。

### ワーカーの起動
ワーカーは

- テストケースの定期実行
- フラグの定期更新
- コンパイル要求の受理
- 実行要求の受理
- コンテナ更新要求の受理

を担当する。

KoHサーバーへの点数送信は`kothcli-client`経由なので、テスト時は`worker/testcase.py`の外部コマンド呼び出し箇所を消す。

`$ ./worker.py`

で起動できる。

サーバー、ワーカーが起動すれば遊べる。

## 環境のリセット
テストで汚した環境をリセットするには

- `config.json`の修正
- `prepare_container.py`でチームコンテナを初期化
- `gen_report.py`で攻撃ログを初期化
- `gen_testcase.py`でデータベースを初期化
- `worker`と`server`の再起動

をすれば良い。

## 動かないときは

[ptr-yudai](https://twitter.com/ptrYudai)に聞くと教えてくれる可能性がある。
