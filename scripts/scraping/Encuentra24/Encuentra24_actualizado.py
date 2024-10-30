import csv
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
# Constantes
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
URL_AUTOS_USADOS = 'https://m.encuentra24.com/panama-es/autos-usados'


XPATH_AUTOS = '//div[contains(@class, "d3-ad-tile d3-ads-grid__item d3-ad-tile--fullwidth")]'
XPATH_MARCA = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Marca')]"
XPATH_MODELO = "//dl[contains(@class,'d3-property-insight__attribute-details')]/dt[text()='Modelo']/following-sibling::dd[1]"
XPATH_ANIO = "//dl[contains(@class, 'd3-property-insight__attribute-details')]/dt[text() = 'Año']/following-sibling::dd[1]"
XPATH_MOTOR = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Motor')]"
XPATH_ESTILO = "//div[contains(@class, 'd3-property-details__detail-label') and normalize-space(text()) = 'Estilo']"
XPATH_ESTILO_DEL_CHASIS = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Estilo del chasis')]"
XPATH_TECHO = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Techo')]"
XPATH_TRANSMISION = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Transmisión')]"
XPATH_COMBUSTIBLE = "//dl[contains(@class,'d3-property-insight__attribute-details')]/dt[text()='Combustible']/following-sibling::dd[1]"
XPATH_ASIENTOS = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Asientos')]"
XPATH_KM = "//dl[contains(@class,'d3-property-insight__attribute-details')]/dt[text()='Kilómetros']/following-sibling::dd[1]"
XPATH_TREN_DE_MANEJO = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Tren')]"
XPATH_TIPO_VENDEDOR = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Tipo de vendedor')]"
XPATH_PROPIETARIO = "//div[@class='d3-propertycontact__address-details']/a"
XPATH_LOCALIZACION = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Localización')]"
XPATH_PUBLICADO = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Publicao')]"
XPATH_PRECIO = "//dl[contains(@class, 'd3-property-insight__attribute-details')]/dt[text() = 'Precio']/following-sibling::dd[1]"

# XPath de botonesb
XPATH_NEXT_BTN = "//div[@class='d3-pagination']/a[contains(@class,'arrow--next')]"
XPATH_RETORNO = "//div[@class='d3-property-toolbar__item'][1]/a"

NUM_PAGINA_DE_INICIO = 1  # Página en la que se empieza a extraer los datos
CANTIDAD_DE_PAGINAS = 5  # Cantidad de páginas que se navegarán para extraer datos

# Configuración del archivo CSV
CSV_FILE = 'test.csv'
CSV_HEADERS = ['Marca', 'Modelo', 'Año', 'Motor', 'Transmision', 'Tren', 'Combustible', 'Asientos', 'KM', 'Precio']


def setup_driver():
    """Sets up the Selenium WebDriver for Chrome."""
    options = webdriver.ChromeOptions()
    options.add_argument("--remote-allow-origins=*")

    try:
        # Initialize the WebDriver without specifying the driver path
        driver = webdriver.Chrome(options=options)
        print("WebDriver setup successful.")
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
    """Obtiene información de los autos en la página actual y la guarda en un archivo CSV."""
    autos_data = []
    try:
        # Espera hasta que la página de los autos cargue
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, XPATH_AUTOS))
        )

        # Lista de los autos por página
        autos = driver.find_elements(By.XPATH, XPATH_AUTOS)
        
        # Iteración sobre la lista de autos
        for index, auto in enumerate(autos):
            try:
                print("Inicio ciclo for lista")
                # Espera hasta que cargue la lista de autos
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, XPATH_AUTOS)))
                auto = driver.find_elements(By.XPATH, XPATH_AUTOS)[index]  # Reobtener el elemento

                driver.execute_script("arguments[0].scrollIntoView(true);", auto)
                auto.click()
                print("despues del click")
                print(driver.current_url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, XPATH_PRECIO))
                )
                marca = driver.find_element(By.XPATH, XPATH_MARCA).text
                modelo = driver.find_element(By.XPATH, XPATH_MODELO).text
                anio = driver.find_element(By.XPATH, XPATH_ANIO).text
                motor = driver.find_element(By.XPATH, XPATH_MOTOR).text
                transmision = driver.find_element(By.XPATH, XPATH_TRANSMISION).text
                combustible = driver.find_element(By.XPATH, XPATH_COMBUSTIBLE).text
                asientos = driver.find_element(By.XPATH, XPATH_ASIENTOS).text
                tren = driver.find_element(By.XPATH, XPATH_TREN_DE_MANEJO).text
                km = driver.find_element(By.XPATH, XPATH_KM).text
                precio = driver.find_element(By.XPATH, XPATH_PRECIO).text

                autos_data.append({'Marca': marca,
                                   'Modelo': modelo,
                                   'Año': anio,
                                   'Motor': motor,
                                   'Transmision': transmision,
                                   'Tren': tren,
                                   'Combustible': combustible,
                                   'Asientos': asientos,
                                   'KM': km, 'Precio': precio})

                print(marca, modelo, anio, motor, transmision, combustible, tren, asientos, km, precio)

                driver.back()

            except StaleElementReferenceException:
                print("Elemento obsoleto encontrado, reintentando...")
                continue  # Salir del bucle interno para refrescar la lista de autos
            except ElementClickInterceptedException:
                print("Elemento no clickable, reintentando...")
                driver.execute_script("arguments[0].scrollIntoView(true);", auto)  # Desplazarse al elemento
                auto.click()
            except NoSuchElementException as e:
                print(f"Error al obtener los detalles del auto: {e}")
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, XPATH_RETORNO))
                )
                btn_retorno = driver.find_element(By.XPATH, XPATH_RETORNO)
                btn_retorno.click()
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")
                break  # Salir del bucle interno para manejar cualquier otro error
    except StaleElementReferenceException:
        print("Lista de autos obsoleta, reintentando...")
    except Exception as e:
        print(f"Ocurrió un error inesperado fuera del bucle: {e}")

    # Guardar los datos obtenidos hasta el momento en el archivo CSV
    if autos_data:
        guardar_en_csv(autos_data, CSV_FILE)


def navegar_pagina(driver, num_pagina_inicio=NUM_PAGINA_DE_INICIO):
    """Navega por las páginas y extrae información de los autos."""
    try:
        if num_pagina_inicio > 1:
            nueva_url = f"{URL_AUTOS_USADOS}.{num_pagina_inicio}"
            print(nueva_url)
            driver.get(nueva_url)
        else:
            driver.get(URL_AUTOS_USADOS)

        for i in range(CANTIDAD_DE_PAGINAS):
            obtener_autos(driver)
            try:
                btn_siguiente = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, XPATH_NEXT_BTN))
                )
                btn_siguiente.click()
            except TimeoutException:
                print("No se encontró el botón siguiente o no se puede hacer clic.")
    except Exception as e:
        print(f"Error navegando a la página {num_pagina_inicio}: {e}")


def main():
    driver = setup_driver()
    try:
        navegar_pagina(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
