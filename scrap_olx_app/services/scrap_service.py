import re, time, os
import pandas as pd
from django.conf import settings as config
from django.http import HttpResponse
from django.utils import timezone as tz
from scrap_olx_app.interfaces.scrap_interface import ScrapOlxInterface
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScrapOlxService(ScrapOlxInterface):
    
    def __init__(self, url: str = None) -> None:

        self.url = url
        # set web driver, ex: safari, chrome, firefox, or edge
        self.webdriver = webdriver.Safari()
        self.webdriver.maximize_window()

    def scrap_olx(self, download: bool = True) -> HttpResponse|Exception:

        if self.url:
            # validate the url
            if self.validate_url():
                self.webdriver.get(url=self.url)

                # load more button on 5 pages 
                for _ in range(1, 5):
                    try:
                        WebDriverWait(driver=self.webdriver, timeout=60).until(method=EC.presence_of_element_located(locator=(By.XPATH, '//*[@id="main_content"]/div/div/section/div/div/div[4]/div[2]/div/div[2]/ul/li/div/button'))).click()
                        time.sleep(3)
                    except Exception as err:
                        print(err)
                        break

                products = []

                # select row of products
                rows = self.webdriver.find_elements(by=By.CSS_SELECTOR, value='#main_content > div > div > section > div > div > div:nth-child(6) > div._2CyHG > div > div:nth-child(2) > ul > li > a > div')
                
                # iterate then get product's information
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

                # if true then download as excel file
                if download:
                    dataframe = pd.DataFrame(data=products)
                    now = tz.now().timestamp()
                    filename = f'data_olx_{now}.xlsx'
                    dataframe.to_excel(excel_writer=f'media/{filename}', index=False)

                    # download to browser
                    file_path = os.path.join(config.MEDIA_ROOT, filename)

                    if os.path.exists(file_path):
                        # with open(file=file_path) as file:
                        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
                        return response
                    else:
                        return HttpResponse(content="File not found.", status=404)

                return "Success"
            else: raise Exception("Error: URL is not valid.")
        else: raise Exception("Error: URL is empty.")
    
    def validate_url(self) -> bool:

        pattern = r'^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$'
        is_valid = bool(re.match(pattern, self.url))
        if is_valid and "olx.co.id" in self.url: return True
        else: return False

    def __del__(self) -> None:
        
        self.webdriver.quit()
        del self.url
        del self.webdriver
