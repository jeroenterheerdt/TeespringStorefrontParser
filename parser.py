from pyquery import PyQuery   
import requests
import json
InputFile = "input/store.html"
 

def getProductImageUrl(product_card_pq):
    product_image_str = str(product_card_pq(".product_card__image"))
    a = product_image_str.find('https://')
    b = product_image_str.find(');" data-reactid')   
    product_image_url = product_image_str[a:b]
    return product_image_url

def getProductCardTitle(product_card_pq):
    return product_card_pq(".product_card__title").text()

def getProductCardProductName(product_card_pq):
    return product_card_pq(".product_card__product_name").text()

def getProductCardPrice(product_card_pq):
    return product_card_pq(".product_card__meta").text()

def getProductCardProductPageUrl(product_card_pq):
    s = str(product_card_pq(".product_card").html())
    a = s.find('https://')
    b = s.find('" data-reactid')
    return s[a:b]

def getProductSizes(product_page_url):
    sizes = {}
    response = requests.get(product_page_url)
    product_page = PyQuery(response.content)
    product_size_drop_down = product_page("#select-size-campaign-page")
    for o in product_size_drop_down.items('option'):
        option_text= o.val('value').text()
        if not option_text == '--':
            o_str = str(o.val('value'))
            if not "disabled" in o_str:
                a_find_str = 'data-usd-price-with-tax="'
                a = o_str.find(a_find_str)
                b = o_str.find('" data-gbp-price="')
                price = o_str[a+len(a_find_str):b]
                sizes.update({option_text:price})
    return sizes

def getProductColors(product_page_url):
    colors = []
    response = requests.get(product_page_url)
    product_page = PyQuery(response.content)
    color_list = product_page(".product__color_list")
    for c in color_list.items('li'):
        col = str(c.html())
        col_find_str = "background-color:"
        a = col.find(col_find_str)
        b = col.find('"/>')
        color_hex = col[a+len(col_find_str):b]
        colors.append(color_hex.upper())
    #deduplicate
    return list(set(colors))

class Product:

    def __init__(self, title, name, price = None, image_url = None, page_url = None, sizes = None, colors = None):
        self.title = title
        self.name = name
        self.price = price
        self.image_url = image_url
        self.page_url = page_url
        self.sizes = sizes
        self.colors = colors

with open(InputFile,encoding="utf8") as f:
    html = f.read()
pq = PyQuery(html)
product_cards = pq(".product_card")
print("Found "+str(len(product_cards))+" products!")
products = []
for product_card in product_cards:
    product_card_pq = PyQuery(product_card)
    
    #product_image_url = getProductImageUrl(product_card_pq)
    product_title = getProductCardTitle(product_card_pq)
    product_name = getProductCardProductName(product_card_pq)
    #product_price = getProductCardPrice(product_card_pq)
    product_page_url = getProductCardProductPageUrl(product_card_pq)
    #sizes = getProductSizes(product_page_url)
    #colors = getProductColors(product_page_url)
    #p = Product(product_title, product_name, product_price, product_image_url, product_page_url, sizes, colors)
    p = Product(product_title, product_name, None, None, product_page_url)
    products.append(p)

print("Parsed "+str(len(products)))