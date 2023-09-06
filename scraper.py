import csv
import time
from datetime import datetime
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium_stealth import stealth
import numpy as np
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    options = webdriver.ChromeOptions()
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # Change chrome driver path accordingly
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    # service = Service(executable_path="./chromedriver")
    # driver = webdriver.Chrome(service=service)
    for i in range(10, 16):
        driver.get(
            f"https://www.cars.com/shopping/results/?list_price_max=&makes[]=&maximum_distance=all&models[]=&page_size=100&page={i}&stock_type=used&zip=")
        element = WebDriverWait(driver, 100) \
            .until(lambda x: x.find_element(By.CLASS_NAME, 'vehicle-card'))

        full_data = []
        elements = [el.get_attribute('href') for el in driver.find_elements(By.CLASS_NAME, 'vehicle-card-link')]
        for el in range(100):
            try:
                data = {}
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(elements[el])
                element = WebDriverWait(driver, 100) \
                    .until(lambda x: x.find_element(By.CLASS_NAME, 'title-section'))
                data['price'] = driver.find_elements(By.CLASS_NAME, 'primary-price')[1].text
                data['name'] = driver.find_elements(By.CLASS_NAME, 'listing-title')[0].text
                mega_elements = driver.find_elements(By.TAG_NAME, "dd")
                data['ext_color'] = mega_elements[0].text
                data['int_color'] = mega_elements[1].text
                data['drivetrain'] = mega_elements[2].text
                try:
                    data['mpg'] = mega_elements[3].find_element(By.CLASS_NAME, "sds-tooltip").find_element(By.TAG_NAME,
                                                                                                           'span').text
                except:
                    print("error 0")
                data['fuel'] = mega_elements[4].text
                data['transmission'] = mega_elements[5].text
                data['engine'] = mega_elements[6].text
                data['mileage'] = mega_elements[9].text
                additional = driver.find_element(By.CLASS_NAME, "vehicle-history-section").find_elements(By.TAG_NAME,
                                                                                                         "dd")
                try:
                    data['accidents'] = additional[0].text
                    data['1owner'] = additional[1].text
                    data['personal_use'] = additional[2].text
                except:
                    print("error occured")
                try:
                    reviews = driver.find_elements(By.CLASS_NAME, "sds-definition-list__value")
                    data['review_comfort'] = reviews[0].text
                    data['review_design'] = reviews[1].text
                    data['review_performance'] = reviews[2].text
                    data['review_value'] = reviews[3].text
                    data['review_styling'] = reviews[4].text
                    data['review_reliability'] = reviews[5].text
                except:
                    print("error occured 2")
                try:
                    data['sellers-notes'] = driver.find_element(By.CLASS_NAME, "sellers-notes").text
                except:
                    print("error occured 3")
                print(data)
                print(el)
                full_data.append(data)
                time.sleep(5)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

        np.save(f'data{i}', np.array(full_data))

    # data = []
    # for i in range(len(elements)):
    #     rand = WebDriverWait(driver, 100) \
    #         .until(lambda x: x.find_elements(By.CLASS_NAME, 'restoran-item'))
    #     elements = driver.find_elements(By.CLASS_NAME, 'restoran-item')
    #     element = elements[i]
    #     element.click()
    #     WebDriverWait(driver, 20) \
    #         .until(lambda x: x.find_elements(By.CLASS_NAME, 'res-comments'))
    #     e = driver.find_elements(By.CLASS_NAME, 'res-comments')[0]
    #     if 'no-comments' in e.get_attribute('class').split():
    #         print('element no comment')
    #         driver.back()
    #         continue
    #     e.click()
    #     rand = WebDriverWait(driver, 100) \
    #         .until(lambda x: x.find_elements(By.CLASS_NAME, 'commentbox'))
    #     for comm in driver.find_elements(By.CLASS_NAME, "commentbox"):
    #         data.append(comm.find_elements(By.TAG_NAME, 'div')[0].text)
    #     driver.back()
    #
    # np.save('data.npy', np.array(data))


def csvfiy():
    all = []
    for i in range(1,12):
        arr = np.load(f"data{i}.npy", allow_pickle=True)
        for ar in arr:
            all.append(ar)
    df = pd.DataFrame(all)
    df.to_csv("full_data.csv")
    print(df.head())


def load():
    df = pd.read_csv("full_data.csv")
    print(df.shape)


if __name__ == "__main__":
    load()
