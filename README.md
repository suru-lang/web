English | [日本語](README_jp.md)

# 屋台 (a web framework for Suru)

A web framework for [Suru (「する」)](https://github.com/suru-lang/suru), a programming language in Japanese. Write a handler for each path (URL), list the routes one per line with 【道】, and you have a server that runs on [suru-lang/http](https://github.com/suru-lang/http). It is written entirely in Suru and works the same in the interpreter and in compiled binaries. Plan: suru-lang/web#1.

## Installing

In a [kumu](https://github.com/suru-lang/suru#building-projects-kumu) project:

```sh
kumu 追加 github.com/suru-lang/web
```

HTTP (suru-lang/http) comes with it as a dependency. Suru 0.10.0 or later is needed (【道】 is a quasi-quote, and 文脈 and 道筋 are records with field types).

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

## Writing routes (【道】)

Under `道群 とは 以下の【道】です`, write one `method pattern handler` per indented line, and close with `以上です`.

- The method is `GET`, `POST`, `PUT`, `PATCH` or `DELETE`.
- The pattern starts with `/`. A `:name` part matches any one part, and `c から 「name」 を 道引数取得する` gives it. A final `*` matches all the remaining parts (its name is `*`).
- The handler is a name like `品表示する` or `品表示すること`.
- Empty lines and everything after `#` are ignored. A wrong line is reported with its line (`【道】の2行目: 道の型『品』は / で始めます`).

A line is the same as `（「GET」 と 「/品/:番号」 と 品表示すること の 道筋）`, which you may also write without 【道】.

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

## Tests

```sh
kumu 試験     # routing, context, responses, middleware, 【道】 (no server)
kumu 点検
```

CI also builds and starts the shop in `例/` and checks its answers with curl.

## Future work

These are the later stages of the plan (suru-lang/web#1).

- Pages: connect with [雛形](https://github.com/suru-lang/template), layouts (a shared frame)
- Turning a JSON body back into a type derived with 【JSON】, and checking form values
- Cookies and sessions, CSRF protection
- Connecting with [台帳](https://github.com/suru-lang/orm): resource routes (list, show, create, update, delete) in one line
- A project template for `kumu 新規 --対象 web`

## License

[MIT](LICENSE)
