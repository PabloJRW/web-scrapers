import csv
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Constantes
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
URL = 'https://m.encuentra24.com/panama-es/autos-usados'
XPATH_NEXT_BTN = '//div[@class="category-paginate--next old-device-flex-fix"]/a'
XPATH_AUTOS = '//li[contains(@class, "hover ann-box-teaser table-view-cell")]'
XPATH_MARCA = './a/div[@class="ann-element--big-photo-wrapper"]/div[@class="ann-element--big-photo-info"]/span'
XPATH_PRECIO = './a/div[@class="ann-element--desciption-big"]/span[@class="ann-element--meta-price"]'
XPATH_ANIO = './a/div[@class="ann-element--big-photo-wrapper"]/div[@class="ann-element--big-photo-info"]/div'


# Asi podemos setear el user-agent en selenium
opts = Options()
opts.add_argument(USER_AGENT)

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
driver.get(URL)


btn_siguiente = driver.find_element(By.XPATH, XPATH_NEXT_BTN)
for i in range(3):
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, XPATH_AUTOS))
    )
    autos = driver.find_elements(By.XPATH, XPATH_AUTOS)
    try:
        print(i)
        for auto in autos:
            marca = auto.find_element(By.XPATH, XPATH_MARCA).text
            precio = auto.find_element(By.XPATH, XPATH_PRECIO).text
            anio = auto.find_element(By.XPATH, XPATH_ANIO).text
            print(f"Marca: {marca}, Precio: {precio}, Año: {anio}")
    except:
        break

    btn_siguiente = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, XPATH_NEXT_BTN))
    )
    btn_siguiente.click()
