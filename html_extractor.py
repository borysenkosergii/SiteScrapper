import re, json
from bs4 import BeautifulSoup

def _clean_website(raw: str) -> str:
    # """
    # • turn 'https:\\/\\/www.example.com\\/page\\/'  ➜  'www.example.com/page/'
    # • works no matter where the \"\\/\" escapes appear
    # """
    # # 1. unescape the slash sequences
    # cleaned = raw.replace(r"\/", "/")
    # # 2. remove every back‑slash that might remain
    # cleaned = cleaned.replace("\\", "")
    # # 3. drop protocol
    # cleaned = re.sub(r"^https?://", "", cleaned, flags=re.I)
    # return cleaned
    return re.sub(r'\\+/', '/', raw)

def get_page_info(html: str) -> dict:
    """
    Return a dict with:
      • EXHIBITOR_ID
      • EXHIBITOR_NAME
      • WEBSITE
      • ADDRESS  (as a dict if JSON‑parsable, else raw string)
      • BOOTH  (text of <a id="newfloorplanlink"> … </a>, or None)
    Missing items appear with value None.
    """
    out = {
        "EXHIBITOR_ID": None,
        "EXHIBITOR_NAME": None,
        "WEBSITE": None,
        "ADDRESS": None,
        "BOOTH": None,
    }

    soup = BeautifulSoup(html, "html.parser")

    # ──────────────────────────────────────────────────────────────
    # 1. pull the <script> block that defines contactinfov3
    script = next(
        (tag for tag in soup.find_all("script")
         if tag.string and "template: '#contactinfo_v3-template'" in tag.string),
        None
    )
    if script and script.string:
        code = script.string

        # locate the object literal returned by data()
        m = re.search(r'return\s*\{', code)
        if m:
            start = m.end() - 1
            depth = 1
            i = start + 1
            while i < len(code) and depth:
                if code[i] == '{':
                    depth += 1
                elif code[i] == '}':
                    depth -= 1
                i += 1
            obj_literal = code[start:i]

            # simple scalar fields
            for key in ("exhid", "exhname", "websiteValue"):
                mm = re.search(fr'\b{key}\s*:\s*"([^"]*)"', obj_literal)
                if mm:
                    val = mm.group(1)
                    out_key = key
                    if key == "websiteValue":
                        val = _clean_website(val)
                    match key:
                        case "exhid":
                            out_key = "EXHIBITOR_ID"
                        case "exhname":
                            out_key = "EXHIBITOR_NAME"
                        case "websiteValue":
                            out_key = "WEBSITE"
                    out[out_key] = val

            # addressValues (already strict JSON)
            mm = re.search(r'addressValues\s*:\s*({[^}]*})', obj_literal, re.S)
            if mm:
                addr = mm.group(1)
                try:
                    out["ADDRESS"] = json.loads(addr)
                except json.JSONDecodeError:
                    out["ADDRESS"] = addr

    # ──────────────────────────────────────────────────────────────
    # 2. text of <a id="newfloorplanlink">
    link = soup.find("a", attrs={"class": "js-exhShowroomLink f4"})
    if link:
        val = link.get_text(strip=True)
        out["BOOTH"] = re.sub(r'—', '-', val)

    return out


# --------------------------------------------------
# Example usage
if __name__ == "__main__":
    with open("page.html", encoding="utf‑8") as f:
        html_doc = f.read()

    info = get_page_info(html_doc)
    print(json.dumps(info, indent=2, ensure_ascii=False))
