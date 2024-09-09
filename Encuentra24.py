import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver # pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Asi podemos setear el user-agent en selenium
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=opts)

driver.get('https://m.encuentra24.com/panama-es/autos-usados')



btn_siguiente = driver.find_element(By.XPATH, '//div[@class="category-paginate--next old-device-flex-fix"]/a')

for i in range(3):
    try:
        btn_siguiente.click()
        sleep(random.uniform(8.0, 10.0))
        btn_siguiente = driver.find_element(By.XPATH, '//div[@class="category-paginate--next old-device-flex-fix"]/a')
        print(i)
    except:
        break

autos = driver.find_elements(By.XPATH, '//li[contains(@class, "hover ann-box-teaser table-view-cell")]')

for auto in autos:
    precio = auto.find_element(By.XPATH, './a/div[@class="ann-element--desciption-big"]/span[@class="ann-element--meta-price"]').text
    print(precio)

    marca = auto.find_element(By.XPATH, './a/div[@class="ann-element--big-photo-wrapper"]/div[@class="ann-element--big-photo-info"]/span').text
    print(marca)

    anio = auto.find_element(By.XPATH,'./a/div[@class="ann-element--big-photo-wrapper"]/div[@class="ann-element--big-photo-info"]/div').text
    print(anio)
