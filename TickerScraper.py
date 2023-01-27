import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict

tickers = []

url = "https://www.slickcharts.com/sp500"

r = httpx.get(url)
html = HTMLParser(r.text)

for i in range(1, 504):
    ticker = html.css_first(f"body > div.container-fluid.maxWidth > div:nth-child(3) > div.col-lg-7 > div > div > table > tbody > tr:nth-child({i}) > td:nth-child(3) > a").text()
    tickers.append(ticker)

print(tickers)

# save tickers to file with 1 ticker per line
with open("tickers.txt", "w") as f:
    f.write("\n".join(tickers))