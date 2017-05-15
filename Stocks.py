import urllib.request, csv

def getStockData(company):
    #url that changes with the company
    url = "http://quote.yahoo.com/d/quotes.csv?s="+company+"&f=sl1d1t1c1ohgvj1pp2owern&e=.csv"

    #opens url, reads it, and closes it
    web_page = urllib.request.urlopen(url)
    read = csv.reader(web_page.read().decode('utf-8').splitlines())
    row = next(read) 
    web_page.close()

    #finds the values and stores them in variables
    last_trade = row[1]
    change = row[4]
    date = row[2]
    open_value = row[5]
    close_value = row[10]

    #returns the variables
    return last_trade, change, date, open_value, close_value


#list of company symbols
companies = ["GOOG","IBM", "LUV", "KO", "CMA",  "COP", "CNX", "COST", "DG", "DFS"]

#runs the function with everything in the list and prints out the text and values
for company in companies:
    values = getStockData(company)
    print("The last trade for",company,"was",values[0],"(" + values[1] + ") on", values[2])
    print("The open was", values[3], "and the previous close was", values[4])
    print()


