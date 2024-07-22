from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv('USER')
password = os.getenv('PASS')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

login_url = "https://app.newtonpaiva.br/FrameHTML/web/app/edu/PortalEducacional/#/login"

notas_url = "https://app.newtonpaiva.br/FrameHTML/web/app/edu/PortalEducacional/#/notas"

driver.get(login_url)

wait = WebDriverWait(driver, 10)
username_field = wait.until(EC.element_to_be_clickable((By.ID, 'User')))
password_field = wait.until(EC.element_to_be_clickable((By.ID, 'Pass')))

username_field.send_keys(user)  
password_field.send_keys(password)    

password_field.send_keys(Keys.RETURN)

wait.until(EC.presence_of_element_located((By.ID, 'btnConfirmar')))

botao_curso = driver.find_element(By.ID, 'item16252498912116681')
botao_curso.click()

confirm_button = driver.find_element(By.ID, 'btnConfirmar')
confirm_button.click()

try:
    wait.until(EC.url_to_be(notas_url))
except:
    driver.get(notas_url)

wait.until(EC.presence_of_element_located((By.XPATH, '//table[@role="grid"]/tbody/tr')))

notas = []
rows = driver.find_elements(By.XPATH, '//table[@role="grid"]/tbody/tr')
for row in rows:
    campus = row.find_element(By.XPATH, './/td[1]/span').text
    curso = row.find_element(By.XPATH, './/td[2]/span').text
    disciplina = row.find_element(By.XPATH, './/td[3]/a').text
    status = row.find_element(By.XPATH, './/td[4]').text
    nota1 = row.find_element(By.XPATH, './/td[5]').text
    nota2 = row.find_element(By.XPATH, './/td[6]').text
    nota_final = row.find_element(By.XPATH, './/td[7]').text
    nota_extra = row.find_element(By.XPATH, './/td[10]').text

    notas.append({
        'campus': campus,
        'curso': curso,
        'disciplina': disciplina,
        'status': status,
        'nota1': nota1,
        'nota2': nota2,
        'nota_final': nota_final,
        'nota_extra': nota_extra
    })

df = pd.DataFrame(notas)
df.to_csv('C:\\Users\\Arthur Coutinho\\Desktop\\Arthur Coutinho\\Python\\teste\\data\\notas.csv', index=False)

# Fechar o navegador
driver.quit()
