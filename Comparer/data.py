from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from scraper import Scraper
from scraper import Selectors
import time

class Googleshop:

    def __init__(self,item:str):
        self.item = item.lower()
        self.productlist = []

        self.webscraper = Scraper(5, True)
        self.webscraper.get("https://www.google.com/shopping")
        time.sleep(0.5)

        searchbox = self.webscraper.find(Selectors.NAME, "q")
        searchbox.clear()
        searchbox.send_keys(self.item + Keys.ENTER)
        time.sleep(0.5)

        spelling = self.webscraper.find(Selectors.CSS_SELECTOR, ".QRYxYe.NNMgCf.AwaEsc")
        if spelling:
            correct = self.webscraper.find_in(spelling, Selectors.TAG_NAME, "a")
            self.item = correct.text.lower()
            
    def getproducts(self):
        try:
            card = self.webscraper.find(Selectors.CSS_SELECTOR, ".gkQHve.SsM98d.RmEs5b")
            self.webscraper.click(card)
            time.sleep(0.5)

            more = self.webscraper.find(Selectors.CLASS_NAME, "fGdMz")
            if more:
                self.webscraper.click(more)
                time.sleep(0.5)
            else:
                return {}

            cards = self.webscraper.find_all(Selectors.CSS_SELECTOR, ".R5K7Cb.SPI3ee.ePEmoc.A63G6.UaVmdb.kno-fb-ctx.PZPZlf.bNtXOd")
        
        except TimeoutError:
            return {}

        for card in cards:

            dic = {}
            product = self.webscraper.find_in(card, Selectors.CSS_SELECTOR, ".Rp8BL.CpcIhb.y1FcZd.rYkzq")
            if product:

                try:
                    price = self.webscraper.find_in(card, Selectors.CSS_SELECTOR, ".QcEgce.qUbqne.WbrF3c")
                    seller = self.webscraper.find_in(card, Selectors.CSS_SELECTOR, ".hP4iBf.gUf0b.uWvFpd")
                    link = self.webscraper.find_in(card, Selectors.CSS_SELECTOR, ".P9159d.hMk97e.BbI1ub")
                    delivery = self.webscraper.find_in(card, Selectors.CSS_SELECTOR, ".OaQPmf.Z8dN6c")

                    dic["product"] = product.text
                    dic["price"] = price.text
                    dic["seller"] = seller.text
                    dic["link"] = link.get_attribute("href")
                    if type(delivery) == list:
                        dic["delivery"] = delivery.text[1]
                    else:
                        dic["delivery"] = delivery.text                
                    self.productlist.append(dic)

                except AttributeError:
                    continue

        self.webscraper.quit()
        return self.productlist

# scraper = Googleshop("unison composition notebook")
# print(scraper.getproducts())