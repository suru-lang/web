English | [日本語](README_jp.md)

# 屋台 (a web framework for Suru)

A web framework for [Suru (「する」)](https://github.com/suru-lang/suru), a programming language in Japanese. Write a handler for each path (URL), list the routes one per line with 【道】, and you have a server that runs on [suru-lang/http](https://github.com/suru-lang/http). It is written entirely in Suru and works the same in the interpreter and in compiled binaries. Plan: suru-lang/web#1.

## Installing

In a [kumu](https://github.com/suru-lang/suru#building-projects-kumu) project:

```sh
kumu 追加 github.com/suru-lang/web
```

HTTP (suru-lang/http), 雛形 (suru-lang/template) and 台帳 (suru-lang/orm) come with it as dependencies. Suru 0.11.0 or later is needed (【道】 is a quasi-quote, 文脈 and 道筋 are records with field types, and sessions are signed with HMAC-SHA256 from 「ハッシュ」).

## Starting a project

`kumu 新規 店 --対象 web` (Suru 0.11.0 or later) creates a web app with everything in place:

```
店/
  組.suru          depends on github.com/suru-lang/web
  本体.suru        opens the server on port 8080
  店.suru          routes (【道】) and handlers
  画面/            templates: 配置.html (the layout) and トップ.html
  公開/            static files (見た目.css)
  試験/道.suru     tests of the routes, without a server
```

- **Develop.** `kumu 実行` builds and runs the app; open http://localhost:8080/. Pages are read from `画面/` on every request, so changes to templates show up without restarting. To skip compiling, run it with the interpreter: `kumu 取得` once, then `suru 本体.suru`.
- **Test.** `kumu 試験` runs `試験/道.suru`, which sends requests straight to `道群` with `振分する`. `kumu 点検` lints the project.
- **Ship.** `kumu 作る` makes the binary `出力/店`. It reads `画面/` and `公開/` from the folder it runs in, so copy those folders next to it and start it there.

## Usage

```
「屋台」 を 読み込んで 使う
「標準」 を 読み込んで 使う

文脈 を トップ表示する は HTTP内の応答 の 動作
c を トップ表示する とは 「いらっしゃいませ、」 + （c から 「お名前」 を 問い取得して HTML逃避する） + 「さん」 を HTML返答する

文脈 を 品表示する は HTTP内の応答 の 動作
c を 品表示する とは 「品 」 + （c から 「番号」 を 道引数取得する） + 「 です」 を 文字返答する

文脈 を 注文受付する は HTTP内の応答 の 動作
c を 注文受付する とは 「/ありがとう?品=」 + （c から 「品」 を 書式取得する） へ 転送返答する

道群 とは 以下の【道】です
  GET  /           トップ表示する
  GET  /品/:番号    品表示する
  POST /注文        注文受付する
以上です

8080 を （道群 を 記録中継すること で 中継付けする） で 屋台開店する
```

A handler is a function that takes a `文脈` (context) and returns an action giving an `HTTP内の応答`. `8080 を 道群 で 屋台開店する` listens on port 8080 and calls the handler of the matching route for each request. The example is [例/店.suru](例/店.suru) (run `kumu 実行` in `例/` and open http://localhost:8080/).

## Examples

- **[例/店.suru](例/店.suru), a small shop.** A menu and order pages made from templates, a form with rules, an order count kept in the session, CSRF tokens, and a JSON API. Run `kumu 実行` in `例/` and open http://localhost:8080/.
- **[例/掲示板/](例/掲示板/), a bulletin board on SQLite.** Posts are stored with 台帳 in `掲示板.db`. The page lists the 20 newest posts, and a form adds or deletes them. The form is checked with rules and protected by CSRF tokens, and the name you wrote is remembered in the session. `資源 /api/投稿 投稿 帳場接続する` adds a JSON API for the same posts. It is its own project (it depends on SQLite): run `kumu 実行` in `例/掲示板/`, and `kumu 試験` for its tests.

## Writing routes (【道】)

Under `道群 とは 以下の【道】です`, write one `method pattern handler` per indented line, and close with `以上です`.

- The method is `GET`, `POST`, `PUT`, `PATCH` or `DELETE`.
- The pattern starts with `/`. A `:name` part matches any one part, and `c から 「name」 を 道引数取得する` gives it. A final `*` matches all the remaining parts (its name is `*`).
- The handler is a name like `品表示する` or `品表示すること`.
- Empty lines and everything after `#` are ignored. A wrong line is reported with its line (`【道】の2行目: 道の型『品』は / で始めます`).

A line is the same as `（「GET」 と 「/品/:番号」 と 品表示すること の 道筋）`, which you may also write without 【道】.

## Pages (雛形)

Pages are written as [雛形](https://github.com/suru-lang/template) templates in a folder (here `画面/`).

```
「屋台」 を 読み込んで 使う
「JSON」 を 読み込んで 使う

画面 とは （「画面」 を 画面設定する） に 「配置.html」 を 配置設定する

品頁 とは 題 は 文字列 で 値段 は 数 の 組
品頁 は 【JSON】 を 導出する

文脈 を 品表示する は HTTP内の応答 の 動作
c を 品表示する とは 「品.html」 を 頁 で 画面 に 画面返答する
ただし 頁 とは （題 は （c から 「名前」 を 道引数取得する） で 値段 は 120 の 品頁） を 品頁JSON化する
```

```
{# 画面/配置.html #}
<!doctype html>
<title>{{ 題 }} - 屋台</title>
<main>{{ 中身 を 生にする }}</main>

{# 画面/品.html #}
<h1>{{ 題 }}</h1>
<p>{{ 値段 }}円</p>
```

- `「画面」 を 画面設定する` uses the templates in the folder 画面. For a 雛形 setting with your own filters or partials, use `設定 を 雛形画面設定する`.
- `画面 に 「配置.html」 を 配置設定する` puts every page inside the layout 配置.html. The layout gets the page's values plus `中身` (the rendered page), and writes it with `{{ 中身 を 生にする }}`.
- `「品.html」 を 値 で 画面 に 画面返答する` is the response action for the page with `値` (a 「JSON」 object) filled in. If the page cannot be rendered, the answer is 500 with the reason. `画面描画する` gives the rendered string as a `成否` instead.
- A record derived with 【JSON】 (`品頁JSON化する`) is a handy way to write the values.

## JSON bodies and forms

A JSON body can be turned straight into a type derived with 【JSON】.

```
注文 とは 品 は 文字列 で 数 は 数 の 組
注文 は 【JSON】 を 導出する

文脈 を 注文受付する は HTTP内の応答 の 動作
c を 注文受付する とは （c を 注文JSON復元すること で JSON本文復元する） を 注文返答すること で 成功時返答する

注文 を 注文返答する は HTTP内の応答 の 動作
o を 注文返答する とは （o を 注文JSON化する） を JSON返答する
```

- `c を JSON本文解析する` gives the body's JSON as a `成否`. `c を 会員JSON復元すること で JSON本文復元する` turns it into the derived type.
- `r を 処理 で 成功時返答する` passes the value of a `成功` to the handler, and answers a `失敗` with 400 and the reason (for example `数が数ではありません`).

Form values are checked with rules (`書式規則`).

```
規則群 とは （「品」 を 必須検査する） と （「数」 を 1 から 9 へ 範囲検査する） と （「備考」 を 200 で 最長検査する）

文脈 を 書式受付する は HTTP内の応答 の 動作
c を 書式受付する とは
  もし 誤り群 = 空 ならば 「/ありがとう」 へ 転送返答する
  そうでなければ 422 と 「品.html」 を （誤り群 を 誤りJSONにする） で 画面 に 画面状態返答する
ただし 誤り群 とは c を 規則群 で 書式検査する
```

- The rules are `必須検査する` (not empty), `数検査する` (a number), `範囲検査する` (a number from … to …), `最長検査する` (at most n characters) and `選択検査する` (one of a list).
- `c を 規則群 で 書式検査する` gives the list of `書式誤り` (field `誤欄` and message `誤文`). An empty list means no errors.
- `誤り群 を 誤りJSONにする` gives a JSON object with the first message for each field, to pass to a page (`{% もし 数 ならば %}{{ 数 }}{% 以上 %}`). `画面状態返答する` answers the page with a status such as 422.

## Cookies, sessions and CSRF

```
秘密 とは 「長くて秘密の文字列です。リポジトリには入れません」 を セッション設定する

文脈 を 回数表示する は HTTP内の応答 の 動作
c を 回数表示する とは （「回数: 」 + （n を 文字列化する） を 文字返答する） に 新値 を 秘密 で セッション保存する
ただし n とは （（c を 秘密 で セッション取得する） から 「回数」 を JSON取得する） を 回数にする
ただし 新値 とは （（「回数」 と （n + 1 の JSON数） の JSON項目） を 空 に 挿入する） の JSON物

JSON を 回数にする は 数
（n の JSON数） を 回数にする とは n
v を 回数にする とは 0

8080 を （道群 を （秘密 で CSRF中継すること） で 中継付けする） で 屋台開店する
```

- `c から 「名」 を クッキー取得する` reads a cookie. `応答の動作 に 「名」 と 値 を クッキー付けする` adds a `Set-Cookie` (`Path=/; HttpOnly; SameSite=Lax`), `クッキー属性付けする` takes your own attributes, and `クッキー消去する` removes one.
- `「…」 を セッション設定する` makes the setting for sessions. `c を 秘密 で セッション取得する` gives the session (a JSON object; an empty object if there is none or the signature does not match), and `応答の動作 に 値 を 秘密 で セッション保存する` signs the value and sets it as a cookie.
- `（秘密 で CSRF中継すること）` is middleware. A GET gets a token in the cookie 屋台札, and `c を CSRF札取得する` gives it to put in forms as `<input type="hidden" name="_札" value="{{ 札 }}">`. A POST, PUT, PATCH or DELETE whose `_札` (or `X-CSRF-Token` header) does not match the cookie gets 403.

## Resource routes (台帳)

A record that derives 【表】 and 【JSON】 becomes a JSON API in one line of 【道】. 台帳 is [suru-lang/orm](https://github.com/suru-lang/orm). The database driver (here SQLite) is added to your own project.

```
「屋台」 を 読み込んで 使う
「JSON」 を 読み込んで 使う
「蔵」 を 読み込んで 使う
「台帳」 を 読み込んで 使う
「SQLite」 を 読み込んで 使う

会員 とは 番号 は 数 で 名前 は 文字列 で 年齢 は 数 の 組

会員 は 【表】 と 【JSON】 を 導出する

帳場接続する は DB接続 の 動作
帳場接続する とは 「店.db」 を SQLite駆動 で DB開封する

道群 とは 以下の【道】です
  資源 /会員  会員 帳場接続する
以上です
```

- `資源 道 組の名前 接続の名前` gives six routes:
  - `GET /会員` lists the records as a JSON array. `?開始=20&上限=10` picks part of the list.
  - `POST /会員` creates a record from the JSON body and answers 201 with the record and `Location: /会員/番号`.
  - `GET /会員/:番号` shows one record.
  - `PUT /会員/:番号` and `PATCH /会員/:番号` update a record from the JSON body.
  - `DELETE /会員/:番号` deletes a record and answers 204.
- A missing record or a 番号 that is not an integer of 1 or more gives 404, and a body that cannot be read or does not fit the type gives 400.
- Without 【道】, write `「/会員」 を （資表 は 会員表 で 資化 は 会員JSON化すること で 資戻 は 会員JSON復元すること で 資開 は （帳場接続する） の 資源） で 資源道群にする`. It gives a list of `道筋`, which can be joined with other routes using `+`.

## Schemas (【スキーマ】)

A type with 【スキーマ】 derived gets its JSON Schema, in the form OpenAPI uses for `components.schemas`. Plan: suru-lang/web#11 (REST APIs like FastAPI).

```
「屋台」 を 読み込んで 使う
「JSON」 を 読み込んで 使う

品 とは 番号 は 数 で 名前 は 文字列 で 値段 は 数 の 組
品 は 【JSON】 と 【スキーマ】 を 導出する

注文 とは 客 は 文字列 で 品群 は 品 の リスト の 組
注文 は 【JSON】 と 【スキーマ】 を 導出する

（注文スキーマ を JSON文字列にする） を 表示する
```

```json
{"type":"object","properties":{"客":{"type":"string"},"品群":{"type":"array","items":{"$ref":"#/components/schemas/_E5_93_81"}}},"required":["客","品群"]}
```

- `品スキーマ` is the schema (a 「JSON」 value). 数 is `number`, 文字列 is `string`, 真偽 is `boolean`, JSON is `{}` (any value) and `X の リスト` is an `array`.
- A field of another derived type is a `$ref` to `#/components/schemas/…`, so that type also derives 【スキーマ】. OpenAPI allows only ASCII letters, digits, `.` and `-` in these keys, so other bytes of the name are written as `_` and two hex digits (品 → `_E5_93_81`); the spec shows the name itself as `title`.
- `品スキーマ群` is the list of `スキーマ定義` (the name `定義名` and the schema `定義図`) of the type and of the types it uses, for the components of a spec.
- A type with two or more forms is a `oneOf` of objects told apart by the item `形`, as 【JSON】 writes it.

## REST APIs (【API】)

With 【API】, a handler is an ordinary function over typed values, not over `文脈`. 屋台 reads and checks the path, query and JSON body from the types you write, calls the handler and answers with JSON, like FastAPI. The handler can use SQL by hand (here with 蔵), the ORM, or no database at all. Plan: suru-lang/web#11.

```
「屋台」 を 読み込んで 使う
「JSON」 を 読み込んで 使う
「蔵」 を 読み込んで 使う
「SQLite」 を 読み込んで 使う

品 とは 番号 は 数 で 名前 は 文字列 で 値段 は 数 の 組
品 は 【JSON】 と 【スキーマ】 を 導出する

新品 とは 名前 は 文字列 で 値段 は 数 の 組
新品 は 【JSON】 と 【スキーマ】 を 導出する

帳場接続する は DB接続 を 返す 入出力動作
帳場接続する とは 「店.db」 を SQLite駆動 で DB開封する

DB接続 で 数 を 品取得する は （品 と API誤り） の 成否 を 返す 入出力動作
db で n を 品取得する とは 以下の手順です
  行群 とは db に 「SELECT 番号, 名前, 値段 FROM 品 WHERE 番号 = ?」 を （（n の DB数） を 空 に 挿入する） で DB差込問合した 結果
  もし 行群 = 空 ならば 「品がありません」 を 404 で API失敗する
  そうでなければ （行群 の 先頭） を 品にして API成功する
  以上です

品API とは 以下の【API】です
  依存 接続 は 帳場接続する で 開き DB閉鎖する で 閉じる
  GET /品/:番号 は 接続 で 番号 を 品取得する
    説明 品を1つ返します
    番号 は 数
    品 を 返す
  GET /品 は 接続 で 開始 から 上限 を 品一覧する
    開始 は 数 で 既定 0
    上限 は 数 で 既定 20
    品 の リスト を 返す
  POST /品 は 接続 で 本文 を 品作成する
    本文 は 新品
    品 を 201 で 返す
以上です

8080 を （品API を 「品屋の API」 で API公開する） で 屋台開店する
```

`品にする`, `品一覧する` and `品作成する` are your own functions like `品取得する`; the whole program, tested with a real SQLite, is [結合試験/試験/品屋API.suru](結合試験/試験/品屋API.suru).

- Write one paragraph per endpoint. The first line is `方法 道 は 処理の呼び方`: the call of the handler as you would write it in する. The indented lines are `名前 は 型` for each input and `型 を 返す` (or `型 を 状態 で 返す`) for the result.
- Where an input comes from is decided by its name: a `:名前` of the path is a path parameter, `本文` is the JSON body, a name in a `依存` line is a dependency, and any other name is a query parameter. Path and query inputs are 数, 文字列 or 真偽 (`true`/`false`); a query input with `で 既定 値` may be left out. The body is a type derived with 【JSON】, or JSON.
- After the type, `で …` clauses add to an input: `で 既定 値` (a default), `で 1 から 9 まで` (a range of numbers), `で 最長 20` and `で 最短 1` (the length of a string), `で 候補 赤 青` (one of these strings), `で 見出し 名前` (read from that request header, not the query) and `で クッキー 名前` (read from that cookie). Without a name, the input's own name is used. A value outside its limits is answered with 422 (`"type":"value_error"`), and the limits and defaults appear in the spec (`minimum`, `maxLength`, `enum`, `default` …). `名前 は 文脈` passes the request itself.

```
見本条件 とは 数 は 数 で 色 は 文字列 で 鍵 は 文字列 の 組

見本API とは 以下の【API】です
  GET /見本 は 条件 を 要求 で 見本表示する
    条件 は 見本条件 の 組
      数 は 数 で 既定 1 で 1 から 9 まで
      色 は 文字列 で 候補 赤 青
      鍵 は 文字列 で 見出し X-API-Key で 最短 3
    要求 は 文脈
    文字列 を 返す
以上です

見本条件 を 文脈 で 見本表示する は （文字列 と API誤り） の 成否 を 返す 入出力動作
条件 を 要求 で 見本表示する とは （条件 の 色） を API成功する
```
- When there are many inputs, `名前 は 組の型 の 組` gathers them into one record: the lines indented under it are its fields, written like other inputs (from the query, a header or a cookie, with the same clauses). The handler gets one value and reads `条件 の 色`; dependencies stay as their own arguments, so partial application such as `店 で 見本表示すること` still works. The fields must match the record type, or the type check fails. In the spec, the fields are parameters of their own.
- `依存 名前 は 開く動作` does that action for each request and passes its value; with `で 開き 閉じる関数 で 閉じる` it also calls the function after the response (here closing the connection). Only the dependencies an endpoint uses are opened, after its inputs are checked.
- The handler returns `（型 と API誤り） の 成否` as an action: end with `x を API成功する`, or `「品がありません」 を 404 で API失敗する`, which is answered with 404 and `{"detail":"品がありません"}`.
- The result is the value as JSON (a type derived with 【JSON】, 数, 文字列, 真偽, JSON, or `X の リスト`) with status 200, or the status you write. 204 has no body.
- Inputs that do not fit their types are answered with 422 before the handler runs, with every error in the form FastAPI uses: `{"detail":[{"loc":["query","開始"],"msg":"数ではありません: x","type":"float_parsing"}]}`.
- `説明 文` and `分類 名前 …` lines in a paragraph give the endpoint's summary and tags in the spec.
- `a を 題 で API公開する` gives the routes plus `GET /openapi.json` (the OpenAPI 3.1 spec, version 0.1.0) and `GET /docs` (Swagger UI). `a を 題 で 版 に API版公開する` sets the version. The types of bodies and results also derive 【スキーマ】 for the spec.
- `a を 題 で 版 に API仕様にする` is the spec as a 「JSON」 value, and `題 を 仕様道 で 元 に API画面頁にする` is the HTML of a Swagger UI page. Swagger UI is loaded from a CDN (`Swagger元`); to load it from elsewhere, make your own `/docs` route with `API画面頁にする`.
- A `資源` line works inside 【API】 too (it is not in the spec yet). `a を API道群にする` gives only the routes, which join other routes with `+`.

## Decisions

1. **A handler is a function, a route is a record.** A handler takes a `文脈` and returns an action giving an `HTTP内の応答`. `道筋` is a record of the method (`道方法`), the pattern (`道型`) and the handler (`道処理`), defined with field types. There are no configuration files or marks in comments.
2. **Routes are tried in order.** `道群 で 要求 を 振分する` calls the handler of the first route whose pattern and method match. If a pattern matches but no method does, the answer is 405 (with the methods in `Allow`); if no pattern matches, it is 404. A HEAD request matches GET routes (HTTP sends only the headers).
3. **Paths are decoded before matching.** The part after `?` and `#` is dropped, the path is split at `/`, and each part has its %XX decoded before it is compared with the pattern. A path that cannot be decoded gets 400. `道引数取得する` gives the decoded string.
4. **Query and form values by name.** `問い取得する` reads the part after `?` in the path, and `書式取得する` reads the body (`application/x-www-form-urlencoded`). `+` becomes a space and %XX is decoded (left as is if it cannot be). If a name appears twice the first one is used; a missing name gives `「」`.
5. **Response helpers return actions.** `文字返答する`, `HTML返答する`, `JSON返答する` (a value of 「JSON」), `状態返答する`, `転送返答する` and `静的返答する` return an action giving an `HTTP内の応答`, so they can be the body of a handler. `転送返答する` is 303 See Other, for use after receiving a form; non-ASCII characters in the target are %XX-encoded.
6. **Middleware wraps handlers.** Middleware is a function that takes a handler and returns a handler. `道群 を 中継 で 中継付けする` wraps the handler of every route. `記録中継する` prints `GET /品/1 200` for each answer.
7. **Static files are served by HTTP.** `「公開」 から 「/静的」 を c で 静的返答する` serves the rest of the path after `/静的` as a file under 公開, with `HTTP内の配信する`. Use it from a route like `GET /静的/* 静的配信する`. HTTP answers 403 to paths that point outside the folder.
8. **Escape values shown in pages.** `HTML逃避する` turns `&`, `<`, `>`, `"` and `'` into character references. Use it when putting query or form values into HTML.
9. **【道】 is `道展開する` in 屋台.** It is the quasi-quote expander (`文字列 を 道展開する は 文字列 の 成否`) and makes an expression for a list of `道筋`. The code it makes uses `道筋` without a prefix, so write `「屋台」 を 読み込んで 使う`.
10. **Pages are 雛形 templates read from files.** `画面返答する` reads the template file on every request, so a changed page shows up without restarting. In `.html` templates, `{{ }}` is HTML-escaped (雛形's automatic escaping).
11. **A layout is a second template.** The page is rendered first, and then the layout is rendered with the page's values plus `中身`. The layout writes `{{ 中身 を 生にする }}` so the page is not escaped twice. 雛形's own inheritance (`継承する`) can also be used inside pages.
12. **A bad JSON body is the client's error.** `成功時返答する` answers a body that cannot be read or does not fit the type with 400 and the reason from 【JSON】's restore function. The Content-Type is not checked.
13. **Form rules are values.** A rule is a `書式規則` record (field name, whether it is required, and a function from the value to a message, `「」` when fine). Rules other than `必須検査する` skip an empty value, so an optional field can still have rules. Messages are in Japanese and name the field.
14. **Sessions live in a signed cookie.** The server keeps nothing: the session is the JSON object in Base64, a `.`, and its HMAC-SHA256 in hexadecimal, in the cookie 屋台. Anyone can read it, but changing it breaks the signature, so don't put secrets in it. Cookies are limited to about 4 KB. Changing the key logs everyone out.
15. **CSRF uses a signed double-submit token.** The token is 16 random bytes from the OS with its signature. It is set as a cookie (not HttpOnly) and must come back in the form or the `X-CSRF-Token` header. GET, HEAD and OPTIONS are not checked, so they should not change anything. Routes such as JSON APIs that don't use cookies can be left out of the middleware.
16. **Signatures are compared in constant time.** Every byte is compared before answering, so timing does not show where a forged signature went wrong.
17. **A resource opens a connection per request.** `資開` is the action that opens a `DB接続`. Each request runs it, uses the connection and closes it, so the database can be changed while the server runs, and requests in different threads don't share a connection.
18. **The first column is the primary key, taken from the path.** When creating, the body's primary key is ignored and the database chooses it. When updating, the 番号 in the path is used. PUT and PATCH both replace every column, so the body must have all the fields except the primary key.
19. **Resource routes are not checked for CSRF by themselves.** They are a JSON API, so leave them out of `CSRF中継する`, or send the token in `X-CSRF-Token`.
20. **Every field of a schema is required.** 【JSON】 writes every field and needs every field to read a value back, so the schema says so too.
21. **Types that refer to each other are not supported yet.** A type may use itself (`木 の リスト` in `木`), but two types that use each other make their `スキーマ群` endless.
22. **An API handler takes typed values.** Where each input comes from is decided by its name and its type is written in the block, so the handler needs no `文脈` and no reading code. There are no annotations or reflection: 【API】 writes ordinary する code.
23. **The written types are checked against the handler.** The call 【API】 writes goes through the type checker, so a block that says `番号 は 数` for a handler that takes a 文字列 is an error before the program runs.
24. **Every input is checked before the handler.** All errors are answered together with 422, in FastAPI's form (`detail`, `loc`, `msg`, `type`) with Japanese messages, so existing clients and tools can read them. `成功時返答する` keeps 400.
25. **Dependencies are opened per request, after the inputs are checked.** A bad request does not open a connection, and a dependency with a closing function is closed after the response is made.
26. **Schema names are encoded in the spec.** OpenAPI allows only `A-Z a-z 0-9 . -` in the keys of `components.schemas`, so a Japanese type name becomes `_E5_93_81`-style bytes, and `title` keeps the real name for Swagger UI.
27. **Swagger UI comes from a CDN, pinned to one version.** 屋台 stays small and the page needs the network; `API画面頁にする` takes another place for the files.
28. **Limits are written in the block, not in the handler.** 屋台 checks them with the types, reports them with the other 422 errors, and puts them in the spec, so the handler only gets values that fit. Header names are compared without case, as HTTP does.
29. **Many inputs go into a record, not into more particles.** A function has only six particles, and past two or three their meaning no longer fits; a record reads its fields by name. Taking inputs as arguments stays the main form, because する applies arguments by particle and partial application keeps working.

## API documentation

The API documentation is made from the comments in `屋台.suru`: the head comment of the file and the comment right above each public definition, written in English. It is published at https://suru-lang-web.readthedocs.io/en/latest/.

```sh
kumu 文書                                                            # writes docs/api/屋台.md
pip install -r docs/requirements.txt && sphinx-build docs docs/_build   # HTML in docs/_build
```

`docs/` and `.readthedocs.yaml` were written by `kumu 文書 --雛形` (Suru 0.11.0 or later). On every build, Read the Docs downloads kumu 0.11.0, runs `kumu 文書 --出力 docs/api` and then Sphinx, so the generated pages are not committed. The editor hover shows the same descriptions.

## Tests

```sh
kumu 試験     # routing, context, responses, middleware, 【道】, pages, JSON bodies, forms, cookies, sessions, CSRF (no server)
kumu 点検
cd 結合試験 && kumu 試験   # resource routes and 【API】 with a real SQLite database (needs SQLite)
```

CI also runs the tests of `例/掲示板/`, builds and starts the shop in `例/` and the bulletin board in `例/掲示板/`, and checks their answers with curl.

## Future work

Candidates after v0.1.0:

- Sessions kept on the server (in a database), for data larger than a cookie
- Resource routes for HTML pages and forms, not only JSON
- Restarting the server when a source file changes during development

## License

[MIT](LICENSE)
