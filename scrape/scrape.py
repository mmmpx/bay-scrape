import sys
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
from datetime import datetime as dt
import json
import logging as log
from collections import defaultdict

from listing import SoldListing
import config


XPATH_LISTINGS      = '//ul[contains(@class, "srp-results")]/li[contains(@class, "s-item") and not(.//*[contains(@class, "s-item__location")])]'
XPATH_NEXT_PAGE     = '//*[contains(@class, "pagination__next")]'

FMT_SOLD_SEARCH_URL = 'https://www.ebay.co.uk/sch/i.html?_fsrp=1&rt=nc&_nkw={}&LH_PrefLoc=1&LH_Complete=1&LH_Sold=1&LH_ItemCondition=1000%7C1500%7C2000%7C2500%7C3000%7C7000&_ipg=240&_blrs=spell_auto_correct'


def sold_search_url(query):
    return FMT_SOLD_SEARCH_URL.format(urllib.parse.quote(query))


def scrape_sold_listing(listing):
    title = listing.title()
    condition = listing.condition()
    type = listing.type()
    price = listing.price()
    sold_date = listing.sold_date()
    seller_info = listing.seller_info()
    url = listing.url()
    
    return {
        'price':                 price['value'],
        'sold_date':             sold_date['value'],
        'type':                  type['value'],
        'condition':             condition['value'],
        'url':                   url['value'],
        'title':                 title['value'],
        'seller':                seller_info['seller'],
        'seller_feedback_count': seller_info['feedback_count'],
        'seller_feedback_score': seller_info['feedback_score'],
        'raw_price':             price['raw'],
        'raw_sold_date':         sold_date['raw'],
        'raw_type':              type['raw'],
        'raw_condition':         condition['raw'],
        'raw_url':               url['raw'],
        'raw_title':             title['raw'],
        'raw_seller_info':       seller_info['raw']
    }


def until(p, it):
    for x in it:
        if p(x): return
        yield x


def adjust_options(driver):
    # Open listing options menu
    driver.find_element(by=By.XPATH, value='//button[contains(@aria-label, "Listing options")]').click()
    driver.find_element(by=By.XPATH, value='//li/button[contains(@aria-label, "Customise")]').click()

    # Set sorting to most recent - newly listed
    select = Select(driver.find_element(by=By.XPATH, value='//select[@id="cust-sort"]'))
    select.select_by_visible_text('Time: newly listed')
    
    # Set to 240 pp even if it's in the URI becuase their website is trash
    driver.find_element(by=By.XPATH, value='//fieldset[contains(@class, "s-customize-form__group") and (./legend[contains(text(), "Items per page")])]/span[contains(@class, "field") and (./label[contains(text(), "240")])]//input').click()

    # Enable all detail options, even if they don't work???
    for field in driver.find_elements(by=By.XPATH, value='//fieldset[contains(@class, "s-customize-form__details")]/span[contains(@class, "field")]'):
        e_chk = field.find_element(by=By.XPATH, value='.//*[local-name() = "svg" and contains(@class, "unchecked")]')
        if e_chk.value_of_css_property('display') != 'none':
            field.click()

    time.sleep(1)
    # Apply changes
    driver.find_element(by=By.XPATH, value='//button[contains(text(), "Apply changes")]').click()


def sold_listings(driver, query, page_delay_s = 0):
    log.info(f'Retrieving sold listings for query: {query}')
    driver.get(sold_search_url(query))
    i = 0
    while True:
        log.info(f'Now on page {i} for query: {query}')
        time.sleep(page_delay_s)
        listings = driver.find_elements(by=By.XPATH, value=XPATH_LISTINGS)
        yield from ({ **scrape_sold_listing(l), 'query': query } for l in map(SoldListing, listings))

        try:
            e_next_page = driver.find_element(by=By.XPATH, value=XPATH_NEXT_PAGE)
            if e_next_page.tag_name == 'button':
                # There's no next page (unintuitively)
                return
            else:
                e_next_page.click()
        except Exception as e:
            log.warn('Breaking early: unable to navigate to the next page')
            log.warn(e)
            # There's no next page, or something bad happened
            return


def scrape_sold_listings(driver, query, until_listing = None, page_delay_s = 0):
    seen_ids = set()
    for l in sold_listings(driver, query, page_delay_s):
        id = l['url'].split('/')[-1]

        if until_listing and until_listing['url'].split('/')[-1] == id:
            log.info(f'Breaking early: reached until_listing')
            return

        # Skip a listing if we've seen it before - they have some last-page = first-page bug? There CAN be a little data loss because of it
        # Should not cause trouble if they fix it, probably good to have anyway
        if id in seen_ids:
            log.info(f'Skipping duplicate listing ({id})')
        else:
            seen_ids.add(id)
            yield l

    # yield from until(
    #     lambda l: until_listing != None and (until_listing['url'] == l['url']),
    #     sold_listings(driver, query, page_delay_s)
    # )


def serialize_sold_listing(listing):
    l2 = { **listing }
    # l2['sold_date'] = l2['sold_date'].strftime('%Y-%m-%d')
    return l2


def update(driver, data, queries):
    by_query = defaultdict(list)
    for l in data:
        by_query[l['query']].append(l)

    data_out = []
    for query in queries:
        most_recent = by_query[query][0] if query in by_query and by_query[query] else None
        rs = scrape_sold_listings(driver, query, until_listing = most_recent, page_delay_s = 5)
        data_out.extend(rs)
        data_out.extend(by_query[query])

    return data_out


def main(argv):
    driver = webdriver.Firefox()
    driver.implicitly_wait(0.5)

    driver.get(sold_search_url('iphone'))
    time.sleep(5)
    driver.find_element(by=By.XPATH, value='//button[@id = "gdpr-banner-decline"]').click()
    adjust_options(driver)
    input('Press ENTER after captcha...')

    print(argv)
    with open(argv[1], 'r') as f:
        data = [json.loads(l) for l in f.read().split('\n') if l]

    data_out = update(driver, data, config.queries)

    # results = []
    # for ls in map(lambda q: scrape_sold_listings(driver, q, page_delay_s = 5), config.queries):
    #     results.extend(ls)

    with open('data_update.jsonl', 'w') as f:
        for l in data_out:
            f.write(json.dumps(serialize_sold_listing(l), ensure_ascii = False))
            f.write('\n')


if __name__ == '__main__':
    log.getLogger().setLevel(log.INFO)
    main(sys.argv)

