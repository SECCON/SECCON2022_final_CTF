# QuickStart

## サーバを起動する
サーバの起動方法

## token

以下がつかえます

```
token1
token2
```

## 問題を登録する

以下の内容を problems.jsonに書いてください。

starttimeは開始時間、tickcountはtickする回数、tickintervalは1tickあたりの時間を表しています。
contentは問題の内容で, `problemlist.py` に書いているproblemClassesのkeyが参照されます。

```
  {
    "model": "witchquiz.Question",
    "pk": 5,
    "fields": {
      "content": "purerandom",
      "starttime": "2023-01-23T01:24:00+09:00",
      "tickcount": 360,
      "tickinterval": "00:00:10"
    }
  }
```

## 提出する

トークンを有効にするために一度スコアボードにログインする必要があります。
以下のようなコードで提出することができます。

```
url = "http://127.0.0.1:8000/api/quiz/"

headers = {'Authorization': 'Token ログイン時に使用したトークン'}

prm = {"answer": [1] * 1024, 'stage': 5}
params = json.dumps(prm)
res = requests.post(url, data=params, headers=headers)

print(json.loads(res.text))
```
