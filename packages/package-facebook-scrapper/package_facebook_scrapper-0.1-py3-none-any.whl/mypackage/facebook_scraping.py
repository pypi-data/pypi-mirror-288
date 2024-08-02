import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
import json
import pickle
import os


class FacebookScraping():
    all_accounts = []

    def __init__(self, all_accounts: list):
        self.random_sec = random.randint(2, 9)
        FacebookScraping.all_accounts = all_accounts
        self.account = None

    def login(self, email, password):
        """The method will login in to account will return logedin driver"""
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--disable-cache")
        options.add_experimental_option("detach", True)
        # options.add_argument("--headless")
        # driver = webdriver.Chrome(options=options)  # Replace with the appropriate WebDriver for your browser
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://www.facebook.com")
        driver.maximize_window()

        # Accept Cookies
        sleep(self.random_sec)
        # cookies_btn = WebDriverWait(driver, 10).until(
        # EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Optionale Cookies ablehnen')]"))
        # )
        # cookies_btn.click()
        # load cookies
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        # Make refresh
        driver.get('https://facebook.com/')
        # Put Email und user Password
        sleep(10)
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "pass")
        login_button = driver.find_element(By.NAME, "login")
        # log in
        email_input.send_keys(email)
        password_input.send_keys(password)
        sleep(3)
        login_button.click()

        return driver

    def scrap_list_of_accounts_html(self, l_driver,
                                    list_of_accounts: list,
                                    num_of_posts: int,
                                    label: bool,
                                    filename: str):

        all_profile = []
        list_span_elements = []

        for self.account in list_of_accounts:
            FacebookScraping.all_accounts.remove(self.account)
            # print the length of the remaining accounts
            print(f"The remaining accounts to scraped: {len(FacebookScraping.all_accounts)}")
            print(f"The account that will be scraped now: {self.account}")
            l_driver.get(f"https://www.facebook.com/{self.account}")
            WebDriverWait(l_driver, 20)

            # Filter the span elements to only include those which contain "View more comments".

            current_profile = {"user": self.account, "label": label}

            # scroll down
            l_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(self.random_sec)
            l_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # scrip given number of posts
            for i in range(1, num_of_posts):
                likes = 0
                comment = 0
                share = 0
                sleep(self.random_sec)
                try:
                    likes = l_driver.find_element(By.XPATH,
                                                  f"//div[@aria-posinset='{i}']//span[@class='x1e558r4']").text
                    print(f"post {i} - likes {likes}")

                except NoSuchElementException:
                    print("no such element")

                try:
                    comments_shares = l_driver.find_elements(By.XPATH,
                                                             f"//div[@aria-posinset='{i}']//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa']")
                    print(
                        f"this are the number of comments and shares: {comments_shares} of Post number: {i} for the Account {self.account}")
                    print(f"The Length of comments and shares {len(comments_shares)}")

                    if len(comments_shares) == 2:
                        """If True mean the post has comments and shares"""
                        comment = comments_shares[0].text
                        share = comments_shares[1].text

                    elif len(comments_shares) == 1 and l_driver.find_elements(By.XPATH,
                                                                              f"//div[@aria-posinset='{i}']//span[@class='x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j']//*[@id]"):
                        """If True mean the post has only comments"""
                        for comments in range(len(comments_shares)):
                            comment = comments_shares[comments].text

                    else:
                        """If True mean the post has only shares"""
                        for ii in range(len(comments_shares)):
                            share = comments_shares[ii].text
                            print(share)

                except NoSuchElementException:
                    print("The post has no Liker or Comments or Shares")

                data = {
                    "num_likes": likes,
                    "num_comments": comment,
                    "num_shares": share
                }
                current_profile[f"post_{i}"] = data
            all_profile.append(current_profile)
            print(f"All profile until now: {list(all_profile)}")

            span_elements = l_driver.find_elements(By.XPATH, '//div[@class="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"]')
            sleep(self.random_sec)

            sleep(self.random_sec)

            for span_element in span_elements:
                list_span_elements.append(span_element.get_property("textContent"))

        with open("posts.html", "w", encoding="utf-8") as file:
            file.write(str(list_span_elements))

        sleep(self.random_sec)

        profile = l_driver.page_source
        with open("index.html", "w", encoding="utf-8") as file:
            file.write(profile)

        if os.path.exists(filename):
            print(f"{filename} file is exits new data will be append")

            with open(filename, "r+") as f:
                file_data = json.load(f)
                file_data.append(all_profile)
            with open(filename, "w") as f:
                json.dump(file_data, f, indent=4)

        else:
            print(f"{filename} doesn't exit new file will be created")
            with open(filename, "w") as f:
                json.dump([all_profile], f, indent=4)

        l_driver.quit()
