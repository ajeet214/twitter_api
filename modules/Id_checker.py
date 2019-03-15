from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import requests
from config import Config

class EmailChecker:

    def _get_proxy(self):
        url = "http://credsnproxy/api/v1/proxy"
        try:
            req = requests.get(url=url)
            if req.status_code != 200:
                raise ValueError
            return req.json()
        except:
            return {"proxy_host": '185.193.36.122',
                        "proxy_port": '23343'}

    def __init__(self):

        self.cred = self._get_proxy()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--incognito")
        # options.add_argument('--proxy-server=socks://' + self.cred['proxy_host'] + ':' + self.cred['proxy_port'])

        # self.driver = webdriver.Chrome(chrome_options=options)

        # remote webdriver
        self.driver = webdriver.Remote(
            command_executor='http://' + Config.SELENIUM_CONFIG['host'] + ':' + Config.SELENIUM_CONFIG[
                'port'] + '/wd/hub',
            desired_capabilities=options.to_capabilities(),
        )

        self.EMAILFIELD = (By.NAME, "account_identifier")
        self.SUBMITBUTTON = (By.CLASS_NAME, "Button EdgeButton--primary EdgeButton")

    def checker(self, emailId):
        url = "https://twitter.com/account/begin_password_reset"
        self.driver.get(url)
        sleep(0.5)
        # print(emailId)

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.EMAILFIELD)).send_keys(emailId)
        # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.SUBMITBUTTON)).click()
        self.driver.find_element_by_xpath('/html/body/div[2]/div/form/input[3]').click()
        # # # print("%s seconds" % (time.time() - start_time))
        sleep(0.5)

        mailid1 = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[1]')
        print(mailid1.text)
        sleep(0.5)
        # return {'mailid': False}
        if 'How do you want to reset your password?' in mailid1.text:
            print('pass')

            self.driver.quit()
            return {'profileExists': True,
                    'contacts': emailId}
        elif "We couldn't find your account with that information" in mailid1.text:
            print('fail')

            self.driver.quit()
            return {'profileExists': False}

        elif "We found more than one account with that phone number" in mailid1.text:
            print('more than one account')

            self.driver.quit()
            return {'profileExists': True,
                    'contacts': emailId}


        # # try:
        # #     mailid1 = self.driver.find_element_by_xpath('//*[@id="app__container
        #

        # "]/div[2]/header')
        # #     sleep(0.5)
        # #     print(mailid1.text)
        # #     self.driver.quit()
        # #
        # #     return {'mailid': False}
        # except:
        #     mailid = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[1]')
        #     print(mailid.text)
        #     self.driver.quit()


if __name__ == '__main__':
    obj = EmailChecker()
    print(obj.checker('justinmat1994@outlook.com'))

# 919166333537
# justinmat1994@outlook.com