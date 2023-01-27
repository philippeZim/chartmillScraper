import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict


@dataclass
class Stock:
    name: str
    ticker: str
    price: float
    PE: float
    totalRating: float
    fundamentalRating: int
    valuationRating: int
    growthRating: int
    profitabilityRating: int
    healthRating: int
    dividendRating: int


tickers = []
with open("tickers.txt", "r") as f:
    tickers = f.read().strip().split("\n")


def getHTML(ticker):
    url = "https://www.chartmill.com/stock/quote/" + ticker + "/profile"
    r = httpx.get(url)
    return HTMLParser(r.text)


def saveHTML(ticker):
    html = getHTML(ticker)
    with open("html.txt", "w") as f:
        f.write(html.html)


def loadHTML():
    with open("html.txt", "r") as f:
        html = HTMLParser(f.read())
    return html


def getStock(html):
    first = html.css_first("h1").text()
    name = first.split("(")[0].strip()
    tickerE = first.split("(")[1].split(")")[0].strip()
    price = first.strip().split(" ")[-3]
    PE = html.css_first("table.table.table-hover.table-lp tr:nth-child(4) span span.font-bold").text().strip()

    fundamental = "rating " + html.css_first("mat-card-content > div:nth-child(2) > div > div > div:nth-child(4) > "
                                             "div.ratings.ng-star-inserted > app-star-rating").attrs["aria-label"]
    valueation = html.css_first("div.table-responsive.ng-star-inserted > table "
                                "> tbody > tr:nth-child(1) > td:nth-child(2) > app-star-rating").attrs["aria-label"]
    growth = html.css_first("div.table-responsive.ng-star-inserted > table "
                            "> tbody > tr:nth-child(1) > td:nth-child(4) > app-star-rating").attrs["aria-label"]
    profitability = html.css_first("div.table-responsive.ng-star-inserted > table "
                                   "> tbody > tr:nth-child(2) > td:nth-child(2) > app-star-rating").attrs["aria-label"]
    health = html.css_first("div.table-responsive.ng-star-inserted > table "
                            "> tbody > tr:nth-child(2) > td:nth-child(4) > app-star-rating").attrs["aria-label"]

    dividend = html.css_first("div.table-responsive.ng-star-inserted > table "
                              "> tbody > tr:nth-child(3) > td:nth-child(2) > app-star-rating").attrs["aria-label"]

    strValues = [fundamental, valueation, growth, profitability, health, dividend]
    values = []
    for i in range(6):
        values.append(int(strValues[i].strip().split(" ")[-1]))
    total = sum(values) / 6
    stock = Stock(name, tickerE, price, PE, total, values[0], values[1], values[2], values[3], values[4], values[5])
    print(asdict(stock))
    # append to file
    with open("stocks.txt", "a") as f:
        f.write(str(asdict(stock)) + "\n")


def main():
    for ticker in tickers:
        html = getHTML(ticker)
        getStock(html)


if __name__ == "__main__":
    main()
