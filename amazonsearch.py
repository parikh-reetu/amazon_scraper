import requests
from bs4 import BeautifulSoup
from csv import writer
import webbrowser

def scrape(urlIn, pageNum, toDo, params):
    dict = {1:'a-offscreen', 2:'a-icon-alt', 3:'a-icon a-icon-prime a-icon-medium'}

    headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    url = 'https://www.amazon.com/s?k=' + urlIn + '&page=' + str(pageNum)
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, features="lxml")

    # products = soup.find_all(class_='a-section a-spacing-medium')
    products = soup.find_all(class_='sg-col-inner')

    with open('amazonproducts.csv', toDo) as csv_file:
        csv_writer = writer(csv_file)
        headers = ['ProductName', 'Price', 'Ratings', "Prime"]
        if (toDo is 'w'):
            csv_writer.writerow(headers)

        for product in products:
            name = product.find(class_='a-size-base-plus a-color-base a-text-normal')
            if name is not None:
                name = name.get_text()
            elif product.find(class_='a-size-medium a-color-base a-text-normal') is not None:
                name = product.find(class_='a-size-medium a-color-base a-text-normal').get_text()
            else:
                continue

            price = product.find(class_='a-offscreen')
            if price is not None:
                price = price.get_text()
            else:
                price = 'None'

            rating = product.find(class_='a-icon-alt')
            if rating is not None:
                rating = rating.get_text()
            else:
                rating = 'None'

            prime = False
            if product.find(class_= 'a-icon a-icon-prime a-icon-medium') is not None:
                prime = True

            csv_writer.writerow([name, price, rating, prime])

def getProduct(urlIn):
    product = urlIn.strip()
    while len(product) is 0:
        product = input('What do you want to search for? ')
        product = product.strip()
    product = product.replace(' ', '+')
    return product

def getParams():
    params = []
    while True:
        temp = input('What information would you like to see? (enter number)\n1. Price\t2. Rating\t3. Prime\ttype "done" to continue\n').strip()
        if temp == 'done':
           break
        elif temp != '':
            params.append(int(temp))
    return params




def main():
    urlIn = getProduct(input('What do you want to search for? '))
    params = getParams()
    pageNum = input('How many pages would you like to search? ')
    scrape(urlIn, 1, 'w', params)
    for i in range(2, int(pageNum)+1):
        scrape(urlIn, i, 'a')
    # GET CHROME WEBPAGE:
    # chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    # webbrowser.get(chrome_path).open(getURL(urlIn, pageNum))
    path = "/Users/reetuparikh/Desktop/CSProjects/webscraping/webscraping-test/amazon/amazonproducts.csv"
    webbrowser.open('file:///' + path)

#RUN 
main()
# print(getParams())

#TESTING
# def test(list):
#     scrape(list[0], 1, 'w')
#     for prod in list[1:]:
#         path="/Users/reetuparikh/Desktop/CSProjects/webscraping/webscraping-test/amazonproducts.csv"
#     webbrowser.open('file:///' + path)
