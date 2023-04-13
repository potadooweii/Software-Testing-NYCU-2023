from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

TIMEOUT = 10

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")

# launch browser
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

driver.get("https://docs.python.org/3/tutorial/index.html")
driver.maximize_window()

# Q2-1
WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/ul/li[7]')))
try:
    ele = driver.find_element(By.XPATH, '/html/body/div[2]/ul/li[7]')
    raw_html = ele.get_attribute('innerHTML')
    ele = Select(ele.find_element(By.ID, "language_select"))
    ele.select_by_value('zh-tw')
finally:
    driver.implicitly_wait(5)
    first_paragraph = driver.find_element(By.XPATH, '//*[@id="the-python-tutorial"]/p[1]').text
    print(first_paragraph)

# Q2-2
search_box = WebDriverWait(driver, TIMEOUT).until(
    lambda d: d.find_element(By.XPATH, '/html/body/div[2]/ul/li[11]/div/form/input[1]')
)
search_box.send_keys('class')
driver.find_element(By.XPATH, '/html/body/div[2]/ul/li[11]/div/form/input[2]').click()

print()
for i in range(1, 6):
    title = WebDriverWait(driver, TIMEOUT).until(
        lambda d: d.find_element(By.XPATH, f'//*[@id="search-results"]/ul/li[{i}]/a')
    ).text
    print(title)