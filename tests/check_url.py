import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
URL_TO_CHECK = "https://m.encuentra24.com/panama-es/autos-usados"

def setup_driver():
    """Configura y devuelve el controlador de Selenium."""
    opts = Options()
    opts.add_argument(f"user-agent={USER_AGENT}")
    opts.add_argument("--headless")  # Ejecuta en modo headless para no abrir una ventana del navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    return driver

def url_status(url):
    """Verifica el estado HTTP de una URL utilizando requests."""
    try:
        response = requests.get(url)
        return response.status_code
    except requests.RequestException:
        return None

def check_url(url):
    """Verifica que la URL se carga correctamente y su estado HTTP es 200."""
    status_code = url_status(url)
    if status_code == 200:
        driver = setup_driver()
        try:
            driver.get(url)
            print("La URL funciona correctamente.")
        finally:
            driver.quit()
    else:
        print("La URL no responde con el estado HTTP 200.")

if __name__ == "__main__":
    # Reemplaza 'URL_A_COMPROBAR' con la URL que deseas verificar
    url_to_check = URL_TO_CHECK
    check_url(url_to_check)
