import csv
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (NoSuchElementException, TimeoutException,
                                        StaleElementReferenceException, NoSuchWindowException)
from selenium.common.exceptions import ElementClickInterceptedException
# Constantes
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
URL_AUTOS_USADOS = 'https://geekymotors.com/dropsc/carros-combustion-electricos?'

XPATH_AUTOS = "//div[@class='drop-container']"
XPATH_NOMBRE = "//h2"
#XPATH_KM = '//div[@class="car-specs"]/div[1]/div[3]'
#XPATH_ESTADO = '//div[@class="car-specs"]/div[2]/div[3]'
#XPATH_COMBUSTIBLE = '//div[@class="car-specs"]/div[3]/div[3]'
XPATH_CARROCERIA = "//div[@class='car-specs']/div/div[contains(@class, 'spec-label') and contains(text(), 'Carrocería')]"
XPATH_TRACCION = "//div[@class='car-specs']/div/div[contains(@class, 'spec-label') and contains(text(), 'Tracción')]"
XPATH_TRANSMISION = "//div[@class='car-specs']/div/div[contains(@class, 'spec-label') and contains(text(), 'Transmisión')]"
#XPATH_ASIENTOS = '//div[@class="car-specs"]/div[8]/div[@class="spec-value"]'
# = '//div[@class="car-specs"]/div[9]/div[@class="spec-value"]'
#XPATH_VERIFICACION = '//div[@class="score-value"]/div/span'
#XPATH_PRECIO = '//div[@class="price-values "]/div'

#CSV_FILENAME = "geeky_motors20.csv"
#CSV_HEADERS = ['Nombre', 'KM', 'Estado', 'Combustible','Carrocería', 'Tracción', 'Transmisión', 'Asientos',
#              'Color', 'Verificación', 'Precio']


def setup_driver():
    opts = webdriver.ChromeOptions()
    # Agrega cualquier opción que necesites
    try:
        # Instalación del ChromeDriver y obtención de la ruta correcta
        driver_path = ChromeDriverManager().install()
        # Corrige la ruta al archivo ejecutable
        correct_driver_path = driver_path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver.exe")
        print(f"Driver path: {correct_driver_path}")  # Verifica la ruta del driver
        driver = webdriver.Chrome(service=Service(correct_driver_path), options=opts)
        return driver
    except Exception as e:
        print(f"Error setting up the driver: {e}")
        raise


def guardar_en_csv(data, filename):
    """Guarda la lista de diccionarios en un archivo CSV sin sobreescribir el contenido existente."""
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)


def obtener_autos(driver):
    """Obtiene información de los autos en la página."""
    autos_geeky = []
    try:
        # Espera a que el checkbox esté en el DOM
        checkbox_nuevos = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="options-states"]/label[1]'))
        )
        print("Checkbox encontrado.")

        if checkbox_nuevos.is_selected():
            print("Checkbox seleccionado. Desmarcando con JavaScript...")
            driver.execute_script("arguments[0].checked = false;", checkbox_nuevos)
            driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", checkbox_nuevos)

            # Espera a que se actualice el DOM
            WebDriverWait(driver, 10).until(
                lambda d: not checkbox_nuevos.is_selected()
            )

        # Bucle para intentar obtener los autos, manejando excepciones
        while True:
            try:
                # Encuentra la lista de autos en la página
                lista_autos = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, XPATH_AUTOS))
                )

                for auto in lista_autos:
                    try:
                        # Haz clic en cada auto
                        driver.execute_script("arguments[0].scrollIntoView(true);", auto)
                        auto.click()

                        # Espera hasta que se cargue la característica específica
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, XPATH_TRACCION))
                        )

                        # Obtén las características del auto
                        nombre = driver.find_element(By.XPATH, XPATH_NOMBRE).text
                        carroceria = driver.find_element(By.XPATH, XPATH_CARROCERIA).text
                        traccion = driver.find_element(By.XPATH, XPATH_TRACCION).text
                        transmision = driver.find_element(By.XPATH, XPATH_TRANSMISION).text

                        print(nombre, carroceria, traccion, transmision)
                        driver.back()

                    except StaleElementReferenceException:
                        print("Elemento obsoleto encontrado, reintentando...")
                        continue
                    except ElementClickInterceptedException:
                        print("Elemento no clickable, reintentando...")
                        driver.execute_script("arguments[0].scrollIntoView(true);", auto)
                        auto.click()
                    except NoSuchElementException as e:
                        print(f"Error al obtener los detalles del auto: {e}")
                        driver.back()

            except StaleElementReferenceException:
                print("Elemento obsoleto en la lista, actualizando la lista de autos...")
                continue
            break

    except Exception as e:
        print(f"Ocurrió un error inesperado fuera del bucle: {e}")
        driver.back()

       

def get_element_text(driver, xpath):
    """Obtiene el texto de un elemento, si no se encuentra, retorna una cadena vacía"""
    try:
        return driver.find_element(By.XPATH, xpath).text
    except NoSuchElementException:
        return ""


def navegar_pagina(driver):
    """
        Navega por una página web usando un botón "siguiente" para avanzar.
    """
    n_page = 1
    while True:
        try:
            next_page = f"{URL_AUTOS_USADOS}page={n_page}"
            driver.get(next_page)

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, XPATH_AUTOS))
            )

            obtener_autos(driver)  # Llama a la función de nuevo para la nueva página
            n_page += 1

        except TimeoutException:
            print("No se encontró el botón siguiente o no se puede hacer click")
            break
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            break


def main():
    driver = setup_driver()
    try:
        driver.get(URL_AUTOS_USADOS)
        navegar_pagina(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
