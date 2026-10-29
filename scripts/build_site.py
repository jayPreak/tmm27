"""Build web/index.html from src/ and plans/. Run after regenerating a plan."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(*p):
    with open(os.path.join(ROOT, *p), encoding="utf-8") as f:
        return f.read()


def embed(name):
    s = json.dumps(json.loads(read("plans", name)), ensure_ascii=False, separators=(",", ":"))
    # No em/en dashes on the page, and never close the <script> tag early.
    return s.replace(" — ", ", ").replace("—", "-").replace("–", "-").replace("</", "<\\/")


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Mumbai Marathon Plans</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Big+Shoulders+Display:wght@600;800&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
"""

body = read("src", "body.html")
body = body.replace("__PLAN_JAYESH__", embed("jayesh-345.json")).replace("__PLAN_OPEN320__", embed("open-320.json"))
page = HEAD + "<style>\n" + read("src", "styles.css") + "</style>\n</head>\n<body>\n" + body + "</body>\n</html>\n"
assert "—" not in page and "–" not in page and "__PLAN" not in page
os.makedirs(os.path.join(ROOT, "web"), exist_ok=True)
with open(os.path.join(ROOT, "web", "index.html"), "w", encoding="utf-8") as f:
    f.write(page)
print("web/index.html", len(page), "bytes")
