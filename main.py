from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
from selenium.webdriver import ActionChains

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://novoseguros.blip.ai/application"
driver.get(url)

def get_start_end_dates():
    # Calcula o primeiro dia do mês e ano atual
    start_date = datetime.now().replace(day=1).strftime('%d/%m/%Y')
    # Calcula o último dia do mês e ano atual
    next_month = datetime.now().replace(day=28) + timedelta(days=4)  # Garante que estamos no próximo mês
    end_date = (next_month - timedelta(days=next_month.day)).strftime('%d/%m/%Y')  # Último dia do mês atual
    return start_date, end_date

start_date, end_date = get_start_end_dates()

try:
    # Aguarda até o campo de email aparecer
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_input.send_keys("lorrayne@novoseguros.com.br")

    # Aguarda até o campo de senha aparecer
    password_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_input.send_keys("Tojefamoki@123")

    # Clica no botão de login
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "blip-login"))
    )
    login_button.click()

    print("Login realizado. Aguardando 20 segundos na página inicial...")
    time.sleep(20)

    # Navega para a página 'home'
    home_url = "https://novoseguros.blip.ai/application/detail/atendimentons/home"
    driver.get(home_url)
    print("Navegou para a página home. Aguardando 20 segundos...")
    time.sleep(20)

    # Navega para a página 'channels'
    channels_url = "https://novoseguros.blip.ai/application/detail/atendimentons/attendance/channels"
    driver.get(channels_url)
    print("Navegou para a página channels. Aguardando 20 segundos...")
    time.sleep(20)

    # Clica no campo ticket pelo xpath fornecido
    ticket_xpath = '//*[@id="helpdesk-menu-history"]/li/a'
    ticket_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, ticket_xpath))
    )
    ticket_button.click()
    print("Clicou no campo ticket.")

    # Aguarda os campos de data aparecerem
    start_date_input = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "datepicker-start-date"))
    )
    end_date_input = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "datepicker-end-date"))
    )

    # Preenche o campo de data inicial usando JavaScript para evitar problemas de máscara
    driver.execute_script("arguments[0].value = '';", start_date_input)
    start_date_input.click()
    for char in start_date:
        start_date_input.send_keys(char)
        time.sleep(0.05)

    # Preenche o campo de data final usando JavaScript para evitar problemas de máscara
    driver.execute_script("arguments[0].value = '';", end_date_input)
    end_date_input.click()
    for char in end_date:
        end_date_input.send_keys(char)
     
    print("Datas preenchidas. O navegador permanecerá aberto.")

    # Clica no botão "send" dentro do shadowRoot via JavaScript
    driver.execute_script("""
        document.querySelector("#send-csv-button").shadowRoot.querySelector("button").click();
    """)
    time.sleep(10)  # Aguarda o clique ser processado
    print("Clicou no botão send email.")
 


 

    input("Pressione Enter para fechar o navegador...")

except Exception as e:
    print("Erro durante o login ou navegação:", e)
    print("Fluxo finalizado. O navegador permanecerá aberto.")
    input("Pressione Enter para fechar o navegador...")

# driver.quit()  # Descomente se quiser fechar manualmente depois