from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

TIMEOUT = 10

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")

# launch browser
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# navigate to NYCU home page
driver.get("https://www.nycu.edu.tw/")

# maximize the window
driver.maximize_window()

# click 新聞
news_href = WebDriverWait(driver, TIMEOUT).until(
    lambda d: d.find_element(By.XPATH, '//*[@id="menu-1-9942884"]/li[2]/a')
)
driver.get(news_href.get_attribute("href"))

# click first news
first_news_id = WebDriverWait(driver, TIMEOUT).until(
    lambda d: d.find_element(By.XPATH, '//*[@id="-tab"]/ul/li[1]')
)
first_news_href = WebDriverWait(driver, TIMEOUT).until(
    lambda d: d.find_element(By.XPATH, '//*[@id="-tab"]/ul/li[1]/a')
)
article_id = first_news_id.get_attribute("id")[3:]
driver.get(first_news_href.get_attribute("href"))

# print the title and content
first_new_title = WebDriverWait(driver, TIMEOUT).until(
    lambda d: d.find_element(By.XPATH, f'//*[@id="{article_id}"]/header/h1')
)
print(first_new_title.text)
first_new_content = WebDriverWait(driver, TIMEOUT).until(
    lambda d: d.find_element(By.XPATH, f'//*[@id="{article_id}"]/div')
)
print(first_new_content.text)

# open a new tab and switch to it
driver.switch_to.new_window("tab")

# navigate to google
driver.get("https://www.google.com/")
search_input = WebDriverWait(driver, TIMEOUT).until(
    lambda d: d.find_element(By.NAME, "q")
)

# input my student number and submit
search_input.send_keys("311551035")
search_input.send_keys(Keys.ENTER)

# print the title of second result
search_results = WebDriverWait(driver, TIMEOUT).until(
    lambda d: d.find_element(By.XPATH, '//*[@id="rso"]/div[3]/div/div/div[1]/div/a/h3')
)
print(search_results.text)

# close the browser
driver.quit()
