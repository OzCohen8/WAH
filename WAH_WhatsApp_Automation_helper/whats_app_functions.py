from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sched
import pyperclip
import datetime
import keyboard


class WhatsAppElements:
    """
    a class which contains path to the html elements
    in case of exceptions this class should be updated
    """
    element_after_load_screen = (By.CSS_SELECTOR, "#side > #pane-side")
    search_box = '//div[@contenteditable="true"][@data-tab="3"]'
    send_box = '//div[@role="textbox"][@contenteditable="true"][@dir="rtl"][@data-tab="10"]'
    online_span = '//span[@class="_2YPr_ i0jNr selectable-text copyable-text"]'
    users_div_class = "_3m_Xw"
    unread_notification_class = "l7jjieqr cfzgl7ar ei5e7seu h0viaqh7 tpmajp1w c0uhu3dl riy2oczp dsh4tgtl sy6s5v3r gz7w46tb lyutrhe2 qfejxiq4 fewfhwl7 ovhn1urg ap18qm3b ikwl5qvt j90th5db aumms1qt"
    username_class = "ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr i0jNr"


class WhatsApp:
    browser = None

    def __init__(self):
        """
        get the browser of whatsapp web running
        waits until the client opens his whatsapp web (scanning QR)
        """
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.browser.get("https://web.whatsapp.com/")  # open WhatsApp web
        try:  # wait till the client open is whatsapp Page
            print("Waiting for a login with QR scan")
            WebDriverWait(self.browser, float("inf")).until(
                EC.presence_of_element_located(WhatsAppElements.element_after_load_screen))
        finally:
            print("logged in successfully")

    def find_chat_person(self, name):
        """
        function that get in specific person or group chat
        :param name: (string) group or person name
        """
        try:
            search = WebDriverWait(self.browser, 4).until(
                EC.presence_of_element_located((By.XPATH, WhatsAppElements.search_box)))
            # copying and pasting the name to handle emoji
            pyperclip.copy(name)
            search.clear()
            search.send_keys(Keys.CONTROL + "v")
            search.send_keys(Keys.ENTER)
        except:
            print("An exception occurred1")

    def send_message(self, send_to, message):
        """
        the function will send a message in a desire chat
        :param send_to: (string) person or group that the message will be sent to
        :param message: (string) the message content
        :param send_on_time: (string 'minutes:hours day.month.year') if added it will send the message in specific time
        """
        # get to the page of the requested person

        self.find_chat_person(send_to)
        try:
            # find send input
            send = WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located((By.XPATH, WhatsAppElements.send_box)))
            # clearing the input in case there is a massege there
            send.clear()
            # handling Emoji's
            pyperclip.copy(message)
            send.send_keys(Keys.CONTROL + "v")
            # send the message
            send.send_keys(Keys.ENTER)
        except:
            print("An exception occurred")

    def send_message_on_time(self, send_to, message, send_on_time):
        # Set up scheduler
        s = sched.scheduler(time.time, time.sleep)
        # Schedule when you want the action to occur
        s.enterabs(time.mktime(time.strptime(send_on_time, "%H:%M %d/%m/%Y")), 0, self.send_message,argument=(send_to, message))
        # Block until the action has been run
        s.run()

    def last_seen(self, name, dast_chat):
        """
        a function which checks repeatedly if a person is online, saves the time he was online
        and send a message in a disire chat to the client
        """
        # if whatsapp has been close but running in background the online will stay active for 15 sec
        # if whatsapp has been fully terminated online status will disappear immediately
        print(f"online check for {name}\nStarting...\npress q to quit --> ", end="")
        online_status, online_string = False, ""
        connected_on = None
        self.find_chat_person(name)
        time.sleep(5)
        while True:
            if keyboard.is_pressed("q"):  # End the function when q entered
                print("\nEnd of function")
                break
            try:
                self.browser.find_element(By.XPATH, WhatsAppElements.online_span)
                if online_status:
                    continue
                online_status = True
                connected_on = datetime.datetime.now()
                online_string = f"{name} is online {connected_on.strftime('%c')}"
            except:
                if not online_status:
                    continue
                connected_finish = datetime.datetime.now()
                online_string = f"{name} is not online,\n connected for {connected_finish - connected_on}"
                online_status = False
            print(online_string)
            self.send_message(dast_chat, online_string)
            self.find_chat_person(name)

    def quit(self):
        """
        the function will close all the tabs and the docker
        """
        self.browser.quit()

    def unread_usernames(self, scrolls=100):
        """
        function which scroll the page as desired and return list of users which sent you a message
        :param scrolls: (int) how much you want to scroll
        :return: (list) list of unread chats
        """
        initial = 10
        usernames = set(())
        for i in range(0, scrolls):
            self.browser.execute_script("document.getElementById('pane-side').scrollTop={}".format(initial))
            soup = BeautifulSoup(self.browser.page_source, "lxml")
            for q in soup.find_all("div", class_=WhatsAppElements.users_div_class):
                if q.find("span", class_=WhatsAppElements.unread_notification_class):
                    username = q.find("span", class_=WhatsAppElements.username_class).text
                    usernames.add(username)
            initial += 10
        return usernames

    def read_all_unread_messages(self):
        """
        a function which reads all unread chats
        """
        print("reading all unread chats..")
        usernames = self.unread_usernames(200)
        for username in usernames:
            self.find_chat_person(username)
        print("all Chats been read")

    def get_last_message_for(self, name):
        messages = list()
        search = self.browser.find_element(*WhatsAppElements.search_box)
        search.send_keys(name + Keys.ENTER)
        time.sleep(3)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        for i in soup.find_all("div", class_="message-in"):
            message = i.find("span", class_="selectable-text")
            if message:
                message2 = message.find("span")
                if message2:
                    messages.append(message2.text)
        messages = list(filter(None, messages))
        return messages