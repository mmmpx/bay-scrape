from datetime import datetime
from selenium.webdriver.common.by import By
import re


# Utility class to scrape data from a "sold listing" element
class SoldListing:

    XPATH_TITLE       = './/*[contains(@class, "s-item__link")]/*[contains(@class, "s-item__title")]'
    XPATH_CONDITION   = './/*[contains(@class, "s-item__subtitle")]/*[contains(@class, "SECONDARY_INFO")]'
    XPATH_TYPE        = './/*[contains(@class, "s-item__bidCount") or contains(@class, "s-item__purchaseOptionsWithIcon") or contains(@class, "s-item__purchaseOptions")]'
    XPATH_PRICE       = './/span[contains(@class, "s-item__price")]'
    XPATH_SOLD_DATE   = './/div[contains(@class, "s-item__caption-section")]//span[@class = "POSITIVE"]'
    XPATH_SELLER_INFO = './/*[contains(@class, "s-item__seller-info-text")]'
    XPATH_URL         = './/a'

    FMT_SOLD_DATE   = '%d %b %Y'

    TYPES = {
        ( lambda s: re.match(r'^Buy it now.*$', s),    0 ),
        ( lambda s: re.match(r'^or Best Offer.*$', s), 1 ),
        ( lambda s: re.match(r'^.*?bids?.*$', s),      2 )
    }

    CONDITIONS = {
        ( lambda s: re.match(r'^(Brand new|New).*$', s), 0 ),
        ( lambda s: re.match(r'^Opened.*$', s),          1 ),
        ( lambda s: re.match(r'^Certified.*$', s),       2 ),
        ( lambda s: re.match(r'^Refurbished.*$', s),     3 ),
        ( lambda s: re.match(r'^Pre-owned.*$', s),       4 ),
        ( lambda s: re.match(r'^Parts.*$', s),           5 )
    }


    def __init__(self, e):
        self.e = e


    def _xpath(self, q):
        return self.e.find_element(by=By.XPATH, value=q)


    def _xpath_S(self, q):
        es = self.e.find_elements(by=By.XPATH, value=q)
        if len(es) == 0: return None
        return es[0]


    # Get the title of this listing
    def title(self):
        e_title = self._xpath(self.XPATH_TITLE)
        raw = e_title.text

        out = raw.replace('\n', ' ')
        return { 'value': out, 'raw': raw }


    # Get the condition of the item listed
    def condition(self):
        e_condition = self._xpath(self.XPATH_CONDITION)
        raw = e_condition.text

        for (f, out) in self.CONDITIONS:
            if f(raw):
                return { 'value': out, 'raw': raw }

        print(f'Failed to parse item condition for: {raw}')
        return { 'value': None, 'raw': raw }


    # Get the type of this listing, e.g. "Buy it now" or auction
    def type(self):
        try:
            e_type = self._xpath(self.XPATH_TYPE)
        except Exception as e:
            print(self.e.get_attribute('innerHTML'))
            raise e
        raw = e_type.text

        for (f, out) in self.TYPES:
            if f(raw):
                return { 'value': out, 'raw': raw }

        print(f'Failed to parse listing type for: {raw}')
        return { 'value': None, 'raw': raw }


    # Get the price at which this listing ended, i.e. at which the item was sold
    def price(self):
        e_price = self._xpath(self.XPATH_PRICE)
        raw = e_price.text

        # remove £ and commas that interfere with float conversion
        clean = e_price.text.replace('£', '').replace(',', '')

        price = None
        if ' to ' in clean:
            # if listing has a price range, best we can do is take the avg
            split = clean.split(' to ')
            price =  sum(map(float, split)) / len(split)
        else:
            price = float(clean)

        return { 'value': price, 'raw': raw }


    # Get the date on which this listing ended
    def sold_date(self):
        e_sold_date = self._xpath(self.XPATH_SOLD_DATE)
        raw = e_sold_date.text

        out = datetime.strptime(raw[5:], self.FMT_SOLD_DATE)
        out = out.strftime('%Y-%m-%d')
        return { 'value': out, 'raw': raw }


    # Get seller information for this listing
    def seller_info(self):
        null = { 'seller': None, 'feedback_count': None, 'feedback_score': None, 'raw': None }
        e_seller_info = self._xpath_S(self.XPATH_SELLER_INFO)
        if e_seller_info == None:
            return null

        raw = e_seller_info.text

        m = re.match(r'^([^ ]+) \(([0-9,]+)\) ([0-9.]+)%$', raw)
        if m == None:
            return { **null, 'raw': raw }

        return { 'seller': m.group(1), 'feedback_count': m.group(2), 'feedback_score': m.group(3), 'raw': raw }


    # Get the URL pointing to this listing
    def url(self):
        e_url = self._xpath(self.XPATH_URL)
        raw = e_url.get_attribute('href')

        out = raw.split('?')[0]
        return { 'value': out, 'raw': raw }

