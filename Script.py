from logging import getLogger, basicConfig, info, INFO
from logging.handlers import TimedRotatingFileHandler
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from rivescript import RiveScript
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from tkinter import messagebox


class WhatsBot(object):
    def __init__(self):
        try:
            basicConfig(format="%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s",
                        filename="../WB_logs/Log.log", datefmt="%m/%d/%Y %I:%M:%S", level=INFO)
            getLogger(__name__).addHandler(TimedRotatingFileHandler("../WB_logs/Log.log", when="midnight", backupCount=10))
            self.bot = RiveScript()
            self.bot.load_directory('dialogues')
            self.bot.sort_replies()
            info("Replies sorted..")
            self.driver = webdriver.Chrome()
            self.chain = ActionChains(self.driver)
            self.driver.get("https://web.whatsapp.com")
            messagebox.showinfo(title='QR Code Scanner',
                                message='Finish on screen 2-step verification, and then click OK.')
            self.source_page()
            info("Server started..")
        except Exception as err:
            raise err

    def source_page(self):
        info("Reloading source page...")
        return BeautifulSoup(self.driver.page_source, "lxml")

    def find_unread_chats(self, soup):
        sender_name = None
        for foo in soup.find_all('div', attrs={'class': '_2EXPL CxUIE'}):
            foo_descendants = foo.descendants
            for d in foo_descendants:
                if d.name == 'div' and d.get('class', '') == ['_25Ooe']:
                    sender_name = d.text
            self.click_chat(sender_name)

    def click_chat(self, sender_name):
        if sender_name in ["Roche SSW", "Hpy Bday RaviTeja", "Cricket Boys", "Penumuli kings", "14 I_Roommates",
                           "LOCAL BOYS", "Falcon fighters'", "Buddies of TeC"]:
            for click_class in self.driver.find_elements_by_class_name('_25Ooe'):
                if click_class.text == sender_name:
                    self.chain.move_to_element(click_class).click().perform()
                    return
        for click_class in self.driver.find_elements_by_class_name('_25Ooe'):
            if click_class.text == sender_name:
                self.chain.move_to_element(click_class).click().perform()
                self.wait_page_to_load()
                self.get_reply(sender_name)

    def get_reply(self, sender_name):
        for unread_msgs in self.source_page().find('div', attrs={'class': '_1mq8g'}).find_next_siblings():
            for msg in unread_msgs.find_all('div', attrs={'class': '_3zb-j ZhF0n'}):
                message_received = msg.text
                reply = self.bot.reply(sender_name, message_received)
                info("My reply to " + sender_name + " is:" + reply)
                self.send_reply(reply)

    def wait_page_to_load(self):
        return WebDriverWait(self.driver, 0).until(
            ec.visibility_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')))

    def send_reply(self, reply):
        self.wait_page_to_load().send_keys(reply + Keys.ENTER)
        self.reach_home()

    def reach_home(self):
        self.source_page()
        for click_class in self.driver.find_elements_by_class_name('_25Ooe'):
            if click_class.text == "Secret Group":
                self.chain.move_to_element(click_class).click().perform()

    def execute(self):
        while True:
            sleep(3)
            self.find_unread_chats(self.source_page())
            self.reach_home()


if __name__ == "__main__":
    try:
        WhatsBot().execute()
    except Exception as exc:
        raise exc
