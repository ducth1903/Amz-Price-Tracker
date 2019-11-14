import requests
from bs4 import BeautifulSoup
import sys
import json

class ProductAmz():
    def __init__(self, soup_obj):
        # Name
        self._name = soup_obj.find(id="productTitle").text.strip()
        if "\"" in self._name: self._name = self._name.replace("\"", "inch")        # this cause error when reading string and when parse JSON to frontend

        # Category 1 and 2
        try:
            category = soup_obj.find("div", id="wayfinding-breadcrumbs_container")
            self._category1 = category.select("li")[0].text.strip()
            self._category2 = category.select("li")[2].text.strip()
        except:
            self._category1, self._category2 = "", ""

        # Price and isDeal
        isBook = soup_obj.find("div", {"id": "dp", "class": {"book"}})
        if isBook:
            self.extract_book_price_helper(soup_obj)
        else:
            self.extract_product_price_helper(soup_obj)

        # Rating and numVotes
        customer_reviews = soup_obj.find("div", id="averageCustomerReviews")
        if customer_reviews:
            self._rating = float(customer_reviews.select("i.a-icon-star")[0].text.strip().split(" ")[0])
            self._nVotes = int(customer_reviews.select("#acrCustomerReviewText")[0].text.strip().split(" ")[0].replace(",", ""))
        else:
            self._rating, self._nVotes = 0.0, 0

        # Availability
        self._availability = soup_obj.find("div", id="availability").text.strip()

        # Get image URL
        isImage = soup_obj.find("img", id="landingImage")
        if isImage:
            # Get the first key of dictionary
            # isImage = {"URL": [dimension_size_of_image]}
            self._imgURL = list(json.loads(isImage["data-a-dynamic-image"]))[0]
        else:
            # try to find different image ID --- this is probably for Book
            isImage2 = soup_obj.find("img", id="imgBlkFront")
            if isImage2:
                self._imgURL = list(json.loads(isImage2["data-a-dynamic-image"]))[0]
            else:
                # if still not able to find image, then return empty string
                self._imgURL = ""
        self.clean_imageURL()

    def getName(self):
        return self._name

    def getPrice(self):
        price_str = self._price[1:]
        if ',' in price_str: price_str = price_str.replace(",", "")     # handle case such as "$1,099.5"
        return float(price_str)

    def getDeal(self):
        return self._isDeal

    def getCategory1(self):
        return self._category1
    
    def getCategory2(self):
        return self._category2

    def getRating(self):
        return self._rating
    
    def getVotes(self):
        return self._nVotes

    def getAvailability(self):
        return self._availability

    def getImageURL(self):
        return self._imgURL

    def clean_imageURL(self):
        # Function to help clean image URL
        if ',' in self._imgURL:
            temp = self._imgURL.split(',')
            self._imgURL = temp[0] + temp[-1]

    def extract_product_price_helper(self, soup_obj):
        try:
            # Deal available
            self._price = soup_obj.find("span", id="priceblock_dealprice").text
            self._isDeal = True
        except:
            # No deal
            temp_price = soup_obj.find("span", id="priceblock_ourprice")
            self._price = temp_price.text if temp_price else soup_obj.find("span", id="priceblock_saleprice").text
            self._isDeal = False

    def extract_book_price_helper(self, soup_obj):
        """ 3 types of displaying prices:
        - One single price (i.e. https://www.amazon.com/Philips-Norelco-AT830-46-Frustration/dp/B00JITDVD2)
        - Three prices in style 1 - div id=centerCol (i.e. https://www.amazon.com/Hundred-Page-Machine-Learning-Book/dp/1999579518)
        - Three prices in style 2 - div class=a-fixed-left-grid (i.e. https://www.amazon.com/Hands-Machine-Learning-Scikit-Learn-TensorFlow/dp/1491962291)
        """
        if soup_obj.find("div", {"id": "centerCol"}):
            """ Three prices style 1 """
            group_prices = soup_obj.find("div", id="MediaMatrix")
            self._price = group_prices.select("span.a-size-base.a-color-price")[0].text.strip()
        else:
            """ Three prices style 2 """
            group_prices = soup_obj.find("div", id="mediaTabsHeadings")
            price = group_prices.select("li.a-active")[0].select("span.mediaTab_subtitle")[0].text.strip()
            if "-" in price:
                # i.e $23 - $28 -> return the lower price
                self._price = price.split(" - ")[0]
            else:
                self._price = price
        self._isDeal = False

def extract_amazon_url(URL):
    '''
    GET HTTP request to desired Amazon URL to get HTML page, then parse to BeautifulSoup to extrace data

    Input: URL (url to the desired Amazon product)
    Output: dict (details of the product: name, price, deal, url)
    '''

    # NOTE: It is essential to specify headers so that it makes requests seem to be coming from a browser, not a script
    # otherwise, will be prevented by CAPTCHA
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "content-type":"text"
    }
    details = {"ASIN": "", "name": "", "price": "", "isDeal": False, "cat1": "", "cat2": "", "rating": 0.0, "nVotes": 0, "availability": "", "imageURL": "", "url": ""}

    if "www.amazon.com" in URL:
        # Trim URL by removing unnecessary parts (i.e. /ref...)  
        ASIN, trimmed_URL = helper_get_ASIN_from_URL(URL, getTrimmedURL=True)

        page = requests.get(trimmed_URL, headers=headers)
        print(f"Page response with {page.status_code}!")
        
        # ''' page.status_code should be 200 (valid page); 503 means CAPTCHA'''
        if page.status_code==200:
            # VALID RESPONSE
            pass
        elif page.status_code==404:
            # INVALID URL
            # raise Exception("The requested page is not valid...")
            return None
        elif page.status_code==503:
            # CAPTCHA RESPONSE
            proxies = get_proxies(country_code="US")                
            for proxy in proxies:
                try:
                    page = requests.get(trimmed_URL, headers=headers, proxies={"https" : proxy, "http" : proxy}, timeout=1)
                except:
                    continue
                if page.status_code == 200:
                    break            

        soup = BeautifulSoup(page.content, "lxml")
        try:
            curr_prod = ProductAmz(soup)
        except:
            ''' Valid Amazon URL but probably not a specific product '''
            return None
        
        details["ASIN"] = ASIN
        details["name"] = curr_prod.getName()
        details["price"] = curr_prod.getPrice()
        details["isDeal"] = curr_prod.getDeal()
        details["cat1"] = curr_prod.getCategory1()
        details["cat2"] = curr_prod.getCategory2()
        details["rating"] = curr_prod.getRating()
        details["nVotes"] = curr_prod.getVotes()
        details["availability"] = curr_prod.getAvailability()
        details["imageURL"] = curr_prod.getImageURL()
        details["url"] = trimmed_URL
    else:
        print("Please enter Amazon link only")
        return None

    return details

def helper_get_ASIN_from_URL(URL, getTrimmedURL=False):
    URL = URL.split("?")[0]
    if "?ref" in URL: URL = URL.replace("?ref", "/ref")
    trimmed_URL = URL.split("/ref")[0]
    ASIN = trimmed_URL.split("/")[-1]
    if getTrimmedURL:
        return ASIN, trimmed_URL
    else:
        return ASIN

def get_proxies(num_proxies=100, country_code=None):
    '''
    Get a pool of Proxies from https://free-proxy-list.net
    so that we don't have to manually copy and paste the proxies as proxies are getting removed frequently
    
    Args:
    num_proxies: # Number of proxies to grab

    Output:
    List of proxies (string): ["IP_ADDRESS:PORT", ...]
    '''
    url_proxy = "https://free-proxy-list.net"

    response = requests.get(url_proxy)
    proxy_soup = BeautifulSoup(response.content, "lxml")
    proxy_table = proxy_soup.find("table", {"id": "proxylisttable"}).select("tbody")[0]
    proxy_table_rows = proxy_table.findAll("tr")
    if country_code:
        list_proxies = ["{0}:{1}".format(proxy_table_rows[i].findAll("td")[0].text, proxy_table_rows[i].findAll("td")[1].text) for i in range(num_proxies) if proxy_table_rows[i].findAll("td")[2]==country_code]
    else:
        list_proxies = ["{0}:{1}".format(proxy_table_rows[i].findAll("td")[0].text, proxy_table_rows[i].findAll("td")[1].text) for i in range(num_proxies)]
    return list_proxies

if __name__ == "__main__":
    # test_url = "https://www.amazon.com/Hundred-Page-Machine-Learning-Book/dp/1999579518"
    # test_url = "https://www.amazon.com/Hands-Machine-Learning-Scikit-Learn-TensorFlow/dp/1491962291"
    # test_url = "https://www.amazon.com/Philips-Norelco-AT830-46-Frustration/dp/B00JITDVD2"
    # test_url = "https://www.amazon.com/dp/B07FZ8S74R/ref=ods_gw_ha_h1_d_dt_rain_T2_091619?pf_rd_p=daa98c3e-e685-4054-a905-c92800ab87c5&pf_rd_r=HMNTAQ39BAYK0MY3B4W8"
    # test_url = "https://www.amazon.com/Hundred-Page-Machine-Learning-Book/dp/1999579518"
    # test_url = "https://www.amazon.com/Apple-iPad-11-inch-Wi-Fi-64GB/dp/B07K344J3N?ref_=ast_sto_dp"
    # test_url = "https://www.amazon.com/Acer-HA220Q-Monitor-Ultra-Thin-Design/dp/B071784D4R?pf_rd_p=5cc0ab18-ad5f-41cb-89ad-d43149f4e286&pd_rd_wg=43IFQ&pf_rd_r=MZK8QF2A55B71VZNRFH0&ref_=pd_gw_wish&pd_rd_w=o4evt&pd_rd_r=c85017da-88cd-4ee3-bcaf-754a3963ffd2"
    test_url = "https://www.amazon.com/gp/product/B07Y8L329S?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=9PS16BHNMKQJM5BTG9X2"
    print(extract_amazon_url(test_url))
    # print(helper_get_ASIN_from_URL(test_url, getTrimmedURL=True))