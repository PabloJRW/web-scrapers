import csv
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Constantes
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
URL = 'https://m.encuentra24.com/panama-es/autos-usados'
XPATH_NEXT_BTN = '//div[@class="category-paginate--next old-device-flex-fix"]/a'
XPATH_AUTOS = '//li[contains(@class, "hover ann-box-teaser table-view-cell")]'
XPATH_MARCA = './a/div[@class="ann-element--big-photo-wrapper"]/div[@class="ann-element--big-photo-info"]/span'
XPATH_PRECIO = './a/div[@class="ann-element--desciption-big"]/span[@class="ann-element--meta-price"]'
XPATH_ANIO = './a/div[@class="ann-element--big-photo-wrapper"]/div[@class="ann-element--big-photo-info"]/div'

# Configuración del archivo CSV
CSV_FILE = 'autos_usados.csv'
CSV_HEADERS = ['Marca', 'Precio', 'Año']


def setup_driver():
    """Configura y devuelve el controlador de Selenium."""
    opts = Options()
    opts.add_argument(f"user-agent={USER_AGENT}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    return driver


def obtener_autos(driver):
    """Obtiene información de los autos en la página actual y la devuelve como lista de diccionarios."""
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, XPATH_AUTOS))
    )
    autos = driver.find_elements(By.XPATH, XPATH_AUTOS)
    autos_data = []
    for auto in autos:
        try:
            marca = auto.find_element(By.XPATH, XPATH_MARCA).text
            precio = auto.find_element(By.XPATH, XPATH_PRECIO).text
            anio = auto.find_element(By.XPATH, XPATH_ANIO).text
            autos_data.append({'Marca': marca, 'Precio': precio, 'Año': anio})
        except NoSuchElementException as e:
            print(f"Error al obtener los detalles del auto: {e}")
    return autos_data


def navegar_pagina(driver):
    """Navega por las páginas y extrae información de los autos, almacenándola en un archivo CSV."""
    driver.get(URL)
    all_autos_data = []
    for i in range(10):
        autos_data = obtener_autos(driver)
        all_autos_data.extend(autos_data)
        try:
            btn_siguiente = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, XPATH_NEXT_BTN))
            )
            btn_siguiente.click()
        except TimeoutException:
            print("No se encontró el botón siguiente o no se puede hacer clic.")
            break
    return all_autos_data


def guardar_en_csv(data, filename):
    """Guarda la lista de diccionarios en un archivo CSV."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(data)


def main():
    driver = setup_driver()
    try:
        autos_data = navegar_pagina(driver)
        guardar_en_csv(autos_data, CSV_FILE)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
