from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Configura el driver
def setup_driver():
    """Configura y devuelve el controlador de Selenium."""
    opts = Options()
    opts.add_argument(f"user-agent={USER_AGENT}")  
    opts.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    return driver


URL_AUTOS_USADOS = 'https://m.encuentra24.com/panama-es/autos-usados'

XPATH_AUTOS = "//div[contains(@class, 'd3-ad-tile--fullwidth')]"
# XPaths para verificar
XPATH_MARCA = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Marca')]"
XPATH_MODELO = "//dl[contains(@class,'d3-property-insight__attribute-details')]/dt[text()='Modelo']/following-sibling::dd[1]"
XPATH_ANIO = "//dl[contains(@class, 'd3-property-insight__attribute-details')]/dt[text() = 'Año']/following-sibling::dd[1]"
XPATH_MOTOR = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Motor')]"
XPATH_TRANSMISION = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Transmisión')]"
XPATH_COMBUSTIBLE = "//dl[contains(@class,'d3-property-insight__attribute-details')]/dt[text()='Combustible']/following-sibling::dd[1]"
XPATH_ASIENTOS = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Asientos')]"
XPATH_KM = "//dl[contains(@class,'d3-property-insight__attribute-details')]/dt[text()='Kilómetros']/following-sibling::dd[1]"
XPATH_TREN = "//div[contains(@class, 'd3-property-details__detail-label') and contains(text(), 'Tren')]"
XPATH_PRECIO = "//dl[contains(@class, 'd3-property-insight__attribute-details')]/dt[text() = 'Precio']/following-sibling::dd[1]"


def verify_xpaths(driver):
    """Obtiene información de los autos en la página actual y la guarda en un archivo CSV."""
    driver.get(URL_AUTOS_USADOS)
    try:
        # Espera hasta que la página de los autos cargue
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, XPATH_AUTOS))
        )
        
        # Lista de los autos por página
        lista_autos = driver.find_elements(By.XPATH, XPATH_AUTOS)
        

        # Iteración sobre la lista de autos
        for index, element in enumerate(lista_autos[:3]):
            try:
                # Espera hasta que cargue la lista de autos
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, XPATH_AUTOS)))
                
                auto = driver.find_elements(By.XPATH, XPATH_AUTOS)[index]  # Reobtener el elemento

                # Desplaza el elemento a la vista
                driver.execute_script("arguments[0].scrollIntoView();", auto)
                
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, XPATH_MARCA))
                )
                print("Hola")
                auto.click()
                
                marca = driver.find_element(By.XPATH, XPATH_MARCA).text
                modelo = driver.find_element(By.XPATH, XPATH_MODELO).text
                anio = driver.find_element(By.XPATH, XPATH_ANIO).text
                motor = driver.find_element(By.XPATH, XPATH_MOTOR).text
                transmision = driver.find_element(By.XPATH, XPATH_TRANSMISION).text
                combustible = driver.find_element(By.XPATH, XPATH_COMBUSTIBLE).text
                asientos = driver.find_element(By.XPATH, XPATH_ASIENTOS).text
                tren = driver.find_element(By.XPATH, XPATH_TREN).text
                km = driver.find_element(By.XPATH, XPATH_KM).text
                precio = driver.find_element(By.XPATH, XPATH_PRECIO).text


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
                driver.back()
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")
                break  # Salir del bucle interno para manejar cualquier otro error
    except StaleElementReferenceException:
        print("Lista de autos obsoleta, reintentando...")
    except Exception as e:
        print(f"Ocurrió un error inesperado fuera del bucle: {e}")


if __name__ == "__main__":
    driver = setup_driver()
    try:
        verify_xpaths(driver)
    finally:
        driver.quit()