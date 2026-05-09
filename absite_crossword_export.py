import requests
from bs4 import BeautifulSoup

BASE = "https://absite.ru/crossw/"

def fetch(url):
    r = requests.get(url, timeout=20)
    r.encoding = r.apparent_encoding
    return r.text


# --------------------------------
# Extract answers
# --------------------------------
def extract_answers(main_html):
    soup = BeautifulSoup(main_html, "html.parser")
    ans = soup.find("div", {"id": "ans"})
    if not ans:
        return "<p>Ответы не найдены.</p>"

    # keep visible
    ans.attrs.pop("style", None)

    # remove scripts, links, buttons
    for t in ans.find_all(["script", "a", "button"]):
        t.decompose()

    return str(ans)


# --------------------------------
# Extract crossword IMAGE and CLUES from print-version page
# --------------------------------
def extract_print_data(print_html):
    soup = BeautifulSoup(print_html, "html.parser")

    # remove junk
    for t in soup.find_all(["script", "a", "button"]):
        t.decompose()

    # image
    img = soup.find("img")
    if img:
        src = img.get("src", "")
        if not src.startswith("http"):
            src = BASE + src.lstrip("/")
        img["src"] = src
        img_html = f'<div class="crossword-image">{img}</div>'
    else:
        img_html = "<p>Изображение не найдено.</p>"

    # clues
    clues = soup.find("div", {"id": "clues"})
    clues_html = str(clues) if clues else "<p>Вопросы не найдены.</p>"

    return img_html, clues_html


#<title>Кроссворд {cid}</title>

# --------------------------------
# Build output HTML
# --------------------------------
def build_html(cid, img, clues, answers):
    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>

<style>
/* Reset body and margins for printing */
body {{
    font-family: sans-serif;
    margin: 0;
    padding: 0.5cm; /* small margin */
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}}

/* Page wrapper for a single crossword */
.crossword-page {{
    display: flex;
    flex-direction: column;
    height: 100vh;  /* full page height for print */
    padding: 0.5cm;
    box-sizing: border-box;
}}

/* Image container */
.crossword-image {{
    display: flex;
    justify-content: center;
    margin-bottom: 0.5cm;
}}

/* Crossword image size */
.crossword-image img {{
    width: 55%;       /* roughly half A4 */
    max-width: none;
    height: auto;
}}

/* Clues */
.block {{
    margin-top: 0.03cm;
}}

/* Answers pinned to bottom */
.answers-block {{
    margin-top: auto;
}}

@media print {{
    body {{
        margin: 0;
        padding: 0.2cm;        /* minimal print margin */
        font-family: sans-serif;
        font-size: 11pt;
        line-height: 1.2;
    }}

    .crossword-page {{
        display: flex;
        flex-direction: column;
        height: 27.7cm;        /* A4 height minus margins */
        width: 19cm;           /* A4 width minus margins */
        page-break-after: always;
        box-sizing: border-box;
    }}

    /* Image at top with almost no whitespace above */
    .crossword-image {{
        display: flex;
        justify-content: center;
        margin: 0;             /* remove top and bottom margins */
        padding-top: 0;        /* remove padding above */
    }}

    .crossword-image img {{
        width: 15cm;           /* grow larger, almost half page width */
        height: auto;
        max-height: 13cm;      /* limit so clues + answers fit below */
        margin: 0;             /* remove default spacing */
    }}

    .clues-block {{
        flex: 1 1 auto;        /* fill remaining space */
        overflow: hidden;      /* prevent pushing answers */
        margin: 0.2cm 0;       /* small spacing around clues */
    }}

    .answers-block {{
        flex-shrink: 0;        /* stick to bottom */
        margin-top: auto;
    }}

    h1, h2 {{
        margin: 0.1cm 0;       /* minimal header spacing */
    }}

    p, b, div {{
        margin: 0;
        padding: 0;
    }}
}}

</style>

</head>
<body>

<div class="block">
<h2>Кроссворд {cid}</h2>
{img}
</div>

<div class="block">
<h2>Вопросы</h2>
{clues}
</div>

<div class="block answers-block">
<h2>Ответы</h2>
{answers}
</div>

</body>
</html>
"""

#<h1>Кроссворд {cid}</h1>

# --------------------------------
# MAIN FUNCTION
# --------------------------------
def export_crossword(cid):
    main_html = fetch(f"{BASE}{cid}.html")

    # find print link
    soup = BeautifulSoup(main_html, "html.parser")
    a = soup.find("a", string=lambda s: s and "Версия" in s)
    if a:
        href = a.get("href")
        print_url = href if href.startswith("http") else BASE + href.lstrip("/")
    else:
        print_url = f"{BASE}{cid}_pic.html"

    print_html = fetch(print_url)

    img, clues = extract_print_data(print_html)
    answers = extract_answers(main_html)

    final = build_html(cid, img, clues, answers)
    outname = f"crossword_{cid}.html"

    with open(outname, "w", encoding="utf-8") as f:
        f.write(final)

    print("Saved:", outname)


# --------------------------------
# Test run
# --------------------------------
if __name__ == "__main__":
    # HISTORY:
    # 6400 to 6500
    for cid in range(5000, 5100):
        export_crossword(cid)
