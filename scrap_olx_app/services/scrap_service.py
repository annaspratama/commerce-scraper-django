import re, time
import pandas as pd
from django.http import HttpResponse
from scrap_olx_app.interfaces.scrap_interface import ScrapOlxInterface
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScrapOlxService(ScrapOlxInterface):
    
    def __init__(self, url: str = None) -> None:

        self.url = url
        self.webdriver = webdriver.Safari()
        self.webdriver.maximize_window()

    def scrap_olx(self, auto_download: bool = True) -> HttpResponse|Exception:

        if self.url:
            if self.validate_url():
                self.webdriver.get(url=self.url)

                # Load more button  
                for _ in range(1, 10):
                    try:
                        WebDriverWait(self.webdriver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main_content"]/div/div/section/div/div/div[4]/div[2]/div/div[2]/ul/li/div/button'))).click()
                        time.sleep(3)
                    except Exception as err:
                        print(err)
                        break

                products = []
                rows = self.webdriver.find_elements(by=By.CSS_SELECTOR, value='#main_content > div > div > section > div > div > div:nth-child(6) > div._2CyHG > div > div:nth-child(2) > ul > li > a > div')
                
                for row in rows:
                    title = row.find_element(by=By.CSS_SELECTOR, value='span._2poNJ').text
                    price = row.find_element(by=By.CSS_SELECTOR, value='span._2Ks63').text
                    subdistrict = row.find_element(by=By.CSS_SELECTOR, value='div._3rmDx > span._2VQu4').text
                    row = {
                        'title': title,
                        'price': price,
                        'subdistrict': subdistrict
                    }
                    products.append(row)

                if auto_download:
                    dataframe = pd.DataFrame(data=products)
                    dataframe.to_excel(excel_writer='exports/data_olx.xlsx', index=False)

                self.webdriver.quit()
                return "Success"
            else: raise Exception("Error: URL is not valid.")
        else: raise Exception("Error: URL is empty.")
    
    def validate_url(self) -> bool:

        pattern = r'^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$'
        is_valid = bool(re.match(pattern, self.url))
        if is_valid and "olx.co.id" in self.url: return True
        else: return False
