from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
import time

# Configuração do navegador
driver_path = r"C:\Users\SAÚDE DIGITAL\Documents\msedgedriver.exe"  # Caminho do Edge WebDriver
url_pec = "https://esus.recife.pe.gov.br/"
service = Service(driver_path)

# Inicializar o navegador
print("Iniciando o navegador")
driver = webdriver.Edge(service=service)
driver.maximize_window()

try:
    # Acessar o site
    print("Acessando o site do PEC")
    driver.get(url_pec)

    # Esperar até que o botão de aceitar cookies esteja visível e clicável
    print("Aceitando cookies")
    aceitar_cookies = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-8wg2g9"))
    )

    # Clicar no botão de aceitar cookies
    aceitar_cookies.click()

    time.sleep(1.5)

    # Fazer login (se necessário)
    username_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
    )

    password_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
    )

    # Preencher o formulário
    print("Preenchendo CPF")
    username_input.send_keys("10096472456")
    print("Preenchendo senha")
    password_input.send_keys("saudedigitalds4")

    # Encontrar o botão de login e clicar
    print("Clicando botão de ACESSAR")
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-cy='LoginForm.access-button']"))
    )
    login_button.click()
    print("Login realizado")

    time.sleep(1.5)

    # Aguardar a página carregar após login
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.css-wstido")))

    # Localizar e clicar na div contendo "Us 106 CS Prof Joaquim Cavalcante"
    print("Localizando a div: US 106 CS Prof Joaquim Cavalcante")
    div_acesso = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//h3[contains(text(),'Us 106 CS Prof Joaquim Cavalcante')]/ancestor::div[@class='css-1djpnbc']"))
    )
    div_acesso.click()
    print("Entrou em US 106 CS Prof Joaquim Cavalcante")

    # Aguardar a barra lateral carregar
    nav_bar = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "nav.css-1csmvn1"))
    )

    # Usar JavaScript para expandir a barra lateral
    driver.execute_script("arguments[0].click();", nav_bar)

    # Aguardar os itens da lista ficarem visíveis
    list_items = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.css-1rvtlej li"))
    )

    # Encontrar o 13º item
    item_13 = list_items[12]

    # Rolar até o item 13 para garantir que ele esteja visível
    driver.execute_script("arguments[0].scrollIntoView(true);", item_13)

    # Aguardar um pequeno tempo para garantir que a rolagem tenha ocorrido
    time.sleep(1)

    # Clicar no 13º item
    print("Entrando em relatórios")
    item_13.click()
    print("Área de relatório aberta")

    # Aguardar as opções de relatórios expandirem
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.css-kdrz0z"))
    )

    # Localizar e clicar no relatório "Cadastro individual"
    print("Clicando em Cadastro Individual")
    cadastro_individual = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Cadastro individual')]"))
    )
    cadastro_individual.click()

    #########################################################
    # Esperar para garantir que a próxima etapa está carregada
    time.sleep(5)

    # Enviar a sequência de teclas
    actions = webdriver.ActionChains(driver)

    # Pressionar Tab 5 vezes com pausas
    for _ in range(6):
        actions.send_keys(Keys.TAB)
        actions.perform()  # Executa a ação
        time.sleep(1.5)  # Pausa de 0.5 segundos entre as teclas

    # Pressionar seta para baixo 4 vezes com pausas
    for _ in range(4):
        actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()  # Executa a ação
        time.sleep(1.5)  # Pausa de 0.5 segundos entre as teclas

    # Pressionar Tab 3 vezes com pausas
    for _ in range(3):
        actions.send_keys(Keys.TAB)
        actions.perform()  # Executa a ação
        time.sleep(1.5)  # Pausa de 0.5 segundos entre as teclas

    # Pressionar Enter 1 vez
    actions.send_keys(Keys.ENTER)
    actions.perform()  # Executa a ação
    time.sleep(1)  # Pausa após o Enter, para ver o efeito

    print("Sequência de teclas enviada com sucesso!")


except Exception as e:
    print(f"Erro durante a execução: {e}")
    import traceback
    traceback.print_exc()  # Isso irá mostrar o traceback completo do erro.

input("Pressione Enter para fechar o navegador...")
driver.quit()
