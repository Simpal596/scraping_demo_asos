from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

DRIVER_PATH = 'D:\chromedriver'
URL = "https://www.asos.com/fr/femme/"

def get_data(driver, product_url):
    try:
        designation = browser.find_element(By.TAG_NAME, "h1").text.split("-")[1].split("-")[0]
    except Exception as e:

        designation = None

    try:
        color = browser.find_element(By.CLASS_NAME, "aKxaq").text
    except:
        color = None

    try:
        category = browser.find_element(By.CSS_SELECTOR,
                                        "#product-details-container > div:nth-child(1) > div > p:nth-child(2) > a:nth-child(1) > strong").text
    except:
        category = None

    try:
        brand = browser.find_element(By.CSS_SELECTOR,
                                     "#product-details-container > div:nth-child(1) > div > p:nth-child(2) > a:nth-child(2) > strong").text
    except:
        brand = browser.find_element(By.TAG_NAME, "h1").text.split("-")[0]

    try:
        collection = browser.find_element(By.CSS_SELECTOR,
                                          "#globalBannerComponent > div > div > div > a:nth-child(1)").text
    except:
        collection = None

    try:
        price = browser.find_element(By.CLASS_NAME, "MwTOW").text
    except:
        price = None

    try:
        product_code = browser.find_element(By.CSS_SELECTOR,
                                            "#product-details-container > div:nth-child(2) > div.product-code > p").text
    except:
        product_code = None

    try:
        description = browser.find_element(By.CSS_SELECTOR,
                                           "#product-details-container > div:nth-child(1) > div > ul").text
    except:
        description = None
    print(f'product_code = {product_code}')
    return product_url,brand,collection,category,color,designation,description,product_code,price

def get_hrefs(driver):
    href_list = []
    anchor_list = driver.find_elements(By.CLASS_NAME, "B36cezB")
    for anchor in anchor_list:
        href_list.append(anchor.get_attribute("href"))
    return href_list
if __name__ == "__main__":
    browser = webdriver.Chrome(executable_path=DRIVER_PATH)
    browser.maximize_window()
    data = pd.DataFrame(columns=[
        "Product_URL",
        "Brand",
        "Collection",
        "Category",
        "Color",
        "Designation",
        "Description",
        "Product Code",
        "Current Price"
    ])
    # browser.get("https://www.asos.com/fr/pullbear/pullbear-blazer-oversize-bleu-de-cobalt/prd/204064132?clr=bleu&colourWayId=204064133&SearchQuery=blazers")
    browser.get(URL)
    WebDriverWait(browser,7).until(EC.presence_of_element_located((By.ID, "chrome-search"))).send_keys("Blazers", Keys.ENTER)
    WebDriverWait(browser,5).until(EC.presence_of_element_located((By.CLASS_NAME, "ApgHkaK")))
    href_list = get_hrefs(browser)
    for href in href_list:
        try:
            browser.get(href)
            print(href)
            print("===============================")
            sleep(2)
            try:
                browser.find_element(By.ID, "onetrust-accept-btn-handler").click()
            except:
                WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "PLUS DE DÉTAILS"))).click()
                WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "about-me")))
        except Exception as e:
            print(e)
            print("something unexpected happened")
            pass
        data.loc[len(data)] = get_data(browser,href)
    browser.close()
    data.to_excel("full_data.xlsx")
