"""「する」のコードに色を付ける Pygments の lexer(kumu 文書 --雛形 が書いたもの)。

conf.py が setup() で app.add_lexer("suru", SuruLexer) として登録します。"""

from pygments.lexer import RegexLexer, bygroups
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String, Text

# ひらがなでない、名前に使える字
_W = r"[^\sぁ-ゟ　（）()「」『』。、#＃※+\-*/%^<>=!−×÷＋－＊／％＾＝≠≦≧≤≥＜＞・]"
_END = r"(?:しましてから|であること|してから|しまして|すること|します|である|でない|した|して|する)"


class SuruLexer(RegexLexer):
    name = "Suru"
    aliases = ["suru", "する"]
    filenames = ["*.suru"]

    tokens = {
        "root": [
            (r"[#＃※].*$", Comment.Single),
            (r"「", String, "string"),
            (r"(『)([^』]*)(』)", bygroups(Punctuation, Name.Function, Punctuation)),
            (r"以下\s*[のは]\s*(?:外部\s*の\s*(?:入出力動作|関数)|(?:入出力)?手順)", Keyword),
            (r"(?:以上|例えば|読み込んで|読み込む|使う|受け取って|返すこと|返します|返す)", Keyword),
            (r"[0-9０-９]+(?:[.．][0-9０-９]+)?", Number),
            (_W + r"+?内の", Name.Namespace),
            (_W + r"+?" + _END, Name.Function),
            (r"(?:そうでなければ|それから|それぞれ|ただし|という|ならば|または|かつ|です|とは|もし)", Keyword),
            (r"(?:から|より|か|が|で|と|に|の|は|へ|を)", Keyword.Pseudo),
            (r"\*\*|[<>=!]=|[+\-*/%^<>=]|[−×÷＋－＊／％＾＝≠≦≧≤≥＜＞]", Operator),
            (r"[()（）。、]", Punctuation),
            (_W + r"+", Name),
            (r"\s+", Text),
            (r".", Text),
        ],
        "string": [
            (r"「", String, "#push"),
            (r"」", String, "#pop"),
            (r"[^「」]+", String),
        ],
    }
