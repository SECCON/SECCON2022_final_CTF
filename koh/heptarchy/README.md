# Heptarchy

## 構成

`distfiles`に配布ファイルがある。

`challenges`にサーバー側のファイルがある。

- `comparator`: diff計算機
- `langs`: 言語ごとの問題一覧
- `server`: サーバー
- `worker`: ワーカー

## デプロイ

魔術

### diff計算機の設定

`comparator`で`./build.sh`を実行する。

### 言語の設定

`langs`以下に各言語の問題を設定する。
フォルダ名は必ずサーバーで設定する`config.json`と整合性をとる。

各言語フォルダの中には次のファイルを置く。

- 配布するコンパイラ
- 問題バイナリ
- 正解コード

配布するものと同じコンパイラのコンテナもビルドしておく。（例：`langs/c/compiler_c`）
コンテナは

```
docker run \
  --rm \
  --network none \
  --name XXXX \
  -v <チーム固有のストレージ>:/tmp \
  イメージ名 /tmp/<ファイル名(langs["code"])>
```

で実行される。必ずファイル名を引数に取り、それをコンパイルした結果を`/tmp`に作るように設計すること。生成されるファイル名は`langs["output"]`と一致する必要がある。

`langs`のキーは以下の通りである。

| キー | 意味 |
|:-:|:-|
| `name` | |
| `code` | アップロード先の名前（ファイル名がバイナリに含まれることがあるので、通常は正解コードと同じファイル名にしておく） |
| `prog` | 問題バイナリのファイル名 |
| `smal` | `.text`セクションのみを比較するか否か |
| `output` | コンパイラのDockerコンテナが生成するファイル名 |
| `ans` | 比較対象のバイナリのファイル名（`smal`がTrueのときは`prog`と異なるはず） |
| `compiler` | 配布するコンパイラのファイル名 |
| `image` | コンパイラのDockerコンテナのタグ |

### redisの起動

```
# apt install redis-server
$ pip install redis
```

### サーバーの起動

```
$ pip install Flask
```

`server/config.json`を適当に変更し、`app.py`を実行する。
本番ではnginxとuwsgiを適当に設定し、`server/uwsgi.ini`を直して動かす。

パスワード（チームトークン）を適当に変更し、`gen_teams.py`でデータベースを初期化する。

### ワーカーの起動
ワーカーは

- ソースコード更新要求の受理
- 定期点数計算

を担当する。

KoHサーバーへの点数送信は`kothcli-client`経由なので、テスト時は`worker/worker.py`の外部コマンド呼び出し箇所を消す。

`$ ./worker.py`

で起動できる。

サーバー、ワーカーが起動すれば遊べる。

## 環境のリセット
テストで汚した環境をリセットするには

- `config.json`の修正
- `gen_teams.py`でデータベースを初期化
- `worker`と`server`の再起動

をすれば良い。

## 動かないときは

[ptr-yudai](https://twitter.com/ptrYudai)に聞くと教えてくれる可能性がある。
