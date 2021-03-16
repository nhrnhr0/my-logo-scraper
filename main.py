from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import sys

def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome('chromedriver.exe',chrome_options=chrome_options )
    return driver

def get_all_catalogs(driver):
    driver.get('http://www.my-logo.co.il/')
    catalogs = driver.find_elements_by_class_name('homepage_catalog_col')
    results = []
    for catalog in catalogs:
        #print(catalog)
        catalog_img = catalog.find_element_by_css_selector('.thumb-info-wrapper img')
        catalog_title = catalog.find_element_by_class_name('homepage_catalog_title')
        a_tag = catalog.find_element_by_css_selector('a.block')

        catalog_title = catalog_title.text
        catalog_img = catalog_img.get_attribute('src')
        a_tag = a_tag.get_attribute('href')

        results.append({
            'img': catalog_img,
            'title': catalog_title,
            'url':a_tag
        })
    return results
def get_products_from_catalog(driver, catalog):
    driver.get(catalog['url'])
    cards = driver.find_elements_by_css_selector('a.block')
    results = []
    items_len = len(cards[1:])
    for i in range(1,items_len):
        cards = driver.find_elements_by_css_selector('a.block')
        card = cards[i]
        #try:
        url = card.get_attribute('href')
        driver.get(url)

        try:

            img = driver.find_element_by_css_selector('.img-responsive')
            caption = driver.find_element_by_css_selector('.product_title')
            makat = driver.find_element_by_css_selector('.product_makat')
            content = driver.find_element_by_css_selector('.product_body')

            img_src = img.get_attribute('src')
            caption_text = caption.text
            makat_text = makat.text
            content = content.text
            result = {
                'img': img_src,
                'caption': caption_text, 
                'makat': makat_text,
                'content': content,
                'url':url,
            }
            results.append(result)
            print(result)
        except:
            print('error: ', sys.exc_info()[0])
            
            
        driver.get(catalog['url'])

        pass# endfor
    return results
'''
    for card in cards[1:]:
        try:
            img = card.find_element_by_css_selector('.thumb-info-wrapper img')
            caption = card.find_element_by_css_selector('.thumb-info-caption .product_thumb_title')
            makat = card.find_element_by_css_selector('.thumb-info-caption .product_thumb_makat')

            img_src = img.get_attribute('src')
            caption_text = caption.text
            makat_text = makat.text
            
            url = card.get_attribute('href')

            body = driver.find_element_by_tag_name("body")
            body.send_keys(Keys.CONTROL + 't')
            driver.get(url)
            content = driver.find_element_by_css_selector('.product_body')
            content = content.text

            results.append({
                'img': img_src,
                'caption': caption_text, 
                'makat': makat_text,
                'content': content,
                'url':url,
            })
            driver.get(catalog['url'])
        except:
            print('error: ', sys.exc_info()[0])

'''
def main():
    driver = init_driver()
    catalogs = get_all_catalogs(driver)
    for catalog in catalogs:
        catalog['products'] = get_products_from_catalog(driver, catalog)
    print('==== DONE ===')
    print(catalogs)
    with open('data.json', 'w') as outfile:
        json.dump(catalogs, outfile)
if __name__ == '__main__':
    main()