# 「屋台」

「屋台」, the web framework of Suru. On top of suru-lang/http, it sends each request to the handler of its route.
Add it with `kumu 追加 github.com/suru-lang/web` and write `「屋台」 を 読み込んで 使う` in your file.
The response type is `HTTP内の応答`, so also write `「HTTP」 を 読み込む` when you use the functions of HTTP.

A handler is a function that takes a `文脈` and gives the action of a response:

```suru
文脈 を 会員表示する は HTTP内の応答 の 動作
c を 会員表示する とは 「会員 」 + （c から 「番号」 を 道引数取得する） を 文字返答する
```

A route is a `道筋` of the method, the path pattern and the handler. With 【道】, write one route per line (see "Usage" in the README): under the line `道群 とは 以下の【道】です`, write indented lines like `GET /会員/:番号 会員表示する`, and close with `以上です`. One line is the same as `（「GET」 と 「/会員/:番号」 と 会員表示すること の 道筋）`.
A 「:名前」 in the path pattern matches one segment, and `道引数取得する` reads it. A 「*」 at the end matches all the rest (its name is 「*」).

`8080 を 道群 で 屋台開店する` listens on port 8080 and calls the handler of the matching route for each request, answering in parallel.

**Pages.** `画面設定する` uses the templates of 「雛形」 in a folder (.html templates escape `{{ }}`). `画面返答する` answers with a page with values put in, and `配置設定する` puts every page in a layout.

**Forms and JSON.** `書式取得する` reads a form field, `書式検査する` checks the fields with rules such as `必須検査する`, and `JSON本文復元する` turns a JSON body into a type derived with 【JSON】.

**Cookies, sessions and CSRF.** Sessions put a JSON object in a signed cookie and keep nothing on the server. `CSRF中継する` refuses a POST and so on whose token does not match, with 403. JSON APIs send the token in the header X-CSRF-Token.

**Resources.** `資源道群にする` makes the six routes of a JSON API for a record type with 【表】 and 【JSON】 derived: GET /会員 (list), POST /会員 (create), and GET, PUT, PATCH and DELETE /会員/:番号. In 【道】 it is one line: `資源 /会員 会員 帳場接続する`.

```{toctree}
:maxdepth: 2
:caption: API
:glob:

api/*
```
