import json
from typing import Any

import requests

# url = "https://sff2025.mapyourshow.com/8_0/ajax/remote-proxy.cfm?action=search&search=United%20States&searchtype=country&show=all"
url = "https://sff2025.mapyourshow.com/8_0/ajax/remote-proxy.cfm?action=search&search=United%20States&searchtype=country&show=exhibitor"
exhibitor_url = "https://sff2025.mapyourshow.com/8_0/exhibitor/exhibitor-details.cfm?exhid="

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "User-Agent": "PostmanRuntime/7.44.0",
    "cookie": "CFID=104007227; CFTOKEN=9b0a730a2cd1ab43-275062CD-CC3F-66FD-DE7459AA03D3D5FB; _ga=GA1.1.1601680550.1750265150; _ga_N77RQK6L8Y=GS2.1.s1750265149$o1$g1$t1750265210$j60$l0$h0",
    "referer": "https://sff2025.mapyourshow.com/8_0/",
    "x-requested-with": "XMLHttpRequest"
}


def read_main_site() -> list[Any]:
    response = requests.get(url, headers=headers)

    json_data = json.loads(response.content)
    # print(json_data["DATA"])
    # print(response.text)

    ids = []
    lst = json_data["DATA"]["results"]["exhibitor"]["hit"]
    for item in lst:
        ids.append(item["fields"]["exhid_l"])
    return ids

def read_exhibitor_html(exhibitor_id: str) -> str:
    response = requests.get(exhibitor_url+exhibitor_id, headers=headers)
    html = json.loads(response.content)["DATA"]["BODYHTML"]

    return html

if __name__ == "__main__":
    # with open("page.html", "w", encoding="utf-8") as f:
    #     f.write(read_exhibitor_html("321755"))

    data = read_main_site()
    i = 0
    for hit in data:
        print(i, " ", hit)
        print(hit["fields"]["exhid_l"])
        i+=1