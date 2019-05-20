from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline as ply

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}

page = 0
listOfPrices = []
xPlot = []
craigsListUrl = 'https://vancouver.craigslist.org/search/van/sub'

minBedrooms = 1
maxBedrooms = 2
minPrice = 100
maxPrice = 100000




def priceFinder(craigsListUrl, page):

	for i in range(1, 26):

		url = (craigsListUrl + '?s='
		+ str(page) + '&min_price=' + str(minPrice) 
		+ '&max_price=' + str(maxPrice) + '&min_bedrooms=' + str(minBedrooms) 
		+ '&max_bedrooms=' + str(maxBedrooms))

		page = page + 120
		print(url)
		response = requests.get(url, headers=headers)
		c = response.content

		soup = BeautifulSoup(c, features='html.parser')

		prices = soup.find_all('span', attrs={'class':'result-price'})

		for price in prices[::2]:
			itemPrice = price.get_text()
			itemPrice = itemPrice.replace("$","")
			if(int(itemPrice) > 0):
				itemPrice = int(itemPrice)
				listOfPrices.append(itemPrice)
				print(itemPrice)

		if(prices == []):
			break

	print(listOfPrices)


def xAxisMaker(xListOfPrices):
	for x in range(0, len(xListOfPrices)):
		xPlot.append(x)


def getAverage(listOfPrices):
	averagePrice = sum(listOfPrices) / float(len(listOfPrices))
	averagePrice = round(averagePrice)
	return averagePrice

priceFinder(craigsListUrl, page)
xAxisMaker(listOfPrices)
print(str(getAverage(listOfPrices)) + ' is the average price')


trace1 = go.Scatter(
	x = xPlot,
	y = listOfPrices,
	mode='markers',
	marker=dict(
        size=10,
        colorscale='Viridis'
    )
)

data = [trace1]

ply.plot(data, filename='index.html')








