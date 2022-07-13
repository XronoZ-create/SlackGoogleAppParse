import seleniumwire.undetected_chromedriver.v2 as uc
import time
import datetime
from requests.utils import requote_uri
from config import Config
from contextlib import suppress

class DeveloperFindApp:
    def __init__(self):
        pass

    def interceptor(self, request, response):
        if "batchexecute" in request.url:
            if request.response.status_code == 200:
                print('success load batch')
                self.success_load_batch = True

    def init_driver(self):
        self.success_load_batch = False
        self.chrome_options = uc.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.driver = uc.Chrome(version_main=Config.VERSION_MAIN, options=self.chrome_options)
        self.driver.response_interceptor = self.interceptor

    def wait_batch(self):
        self.date_start = datetime.datetime.now()
        while True:
            if (datetime.datetime.now() - self.date_start) >= datetime.timedelta(seconds=2):
                print("Долго ждем загрузку batch")
                raise Exception
            if self.success_load_batch:
                self.success_load_batch = False
                break
            time.sleep(1)

    def find_app(self, dev_href):  # dev_type: [dev, developer]
        """ Поиск приложений разработчика """

        try:
            self.driver.get(dev_href)
        except:  # Если крашнут драйвер или не создан
            self._end()
            self.init_driver()
            self.driver.get(dev_href)

        for _ in range(1, 30):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            with suppress(Exception):
                self.driver.find_element_by_xpath("//button[@aria-label='Show more']").click()
            try:
                self.wait_batch()
                time.sleep(2)
            except:
                break
        for _ in range(1, 30):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.driver.find_element_by_xpath("//button[@aria-label='Show more']").click()
                self.wait_batch()
                time.sleep(2)
            except:
                break

        self.app_xpath = self.driver.find_elements_by_xpath("//a[starts-with (@href,'/store/apps/details?id=')]")
        self.list_app = []
        for self.one_app_xpath in self.app_xpath:
            self.list_app.append(
                self.one_app_xpath.get_attribute('href').split('/store/apps/details?id=')[1]
            )
        return self.list_app


    def _end(self):
        try:
            self.driver.quit()
        except:
            pass




