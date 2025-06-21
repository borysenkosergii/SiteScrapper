import json
import html_extractor
import site_reader
from concurrent.futures import ThreadPoolExecutor

def process_page(id: str) -> dict:
    html = site_reader.read_exhibitor_html(id)
    info = html_extractor.get_page_info(html)
    print(info)
    return info

if __name__ == "__main__":
    ids = site_reader.read_main_site()

    with ThreadPoolExecutor(max_workers=20) as pool:
        results = list(pool.map(process_page, ids))

    with open("results.json", "w", encoding="utf‑8") as f:
        f.write(json.dumps(results, ensure_ascii=True, indent=4))

    # print(json.dumps(results, indent=4))
    # print(len(results))

