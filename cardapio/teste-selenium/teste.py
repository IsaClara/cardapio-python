from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os

#variável da url
caminho_html_login = 'http://127.0.0.1:8000/login/'

#injeta o drive do selenium no chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# 1. TELA DE LOGIN
driver.get(caminho_html_login)

#Variáveis da model
loginUsuario = driver.find_element(By.ID, 'id_username')
senhaUsuario = driver.find_element(By.ID, 'id_password')


login = {'loginUsuario':'Ana'}
senha = {'senhaUsuario':'123'}

#adicionando valores aos inputs do modal
loginUsuario.send_keys(login['loginUsuario'])
time.sleep(2)
senhaUsuario.send_keys(senha['senhaUsuario'])
time.sleep(2)
driver.find_element(By.ID, 'botao-entrar').click()
time.sleep(3)

# 2. TELA DE DASHBOARD (Aba Editar Itens)
driver.find_element(By.ID, 'editarItens').click()
time.sleep(3)

# --- ADICIONANDO SEGUNDA CATEGORIA: Pizza ---
categoria_nome = driver.find_element(By.ID, 'nome_cat')
categoria_nome.send_keys('Pizza')
time.sleep(2)

'''
btnAdicionar = driver.find_element(By.ID, 'adicionar_cat')
btnAdicionar.click()
'''

select_cat = Select(driver.find_element(By.ID, "id_cat_select"))
try:
    select_cat.select_by_visible_text('Hamburguer')
except:
    select_cat.select_by_index(0)

# Preenchendo o Nome do Alimento
nome_comida_cat = driver.find_element(By.ID, 'nome_comida')
nome_comida_cat.send_keys('X-burguer')
time.sleep(2)

## Preenchendo a Descrição
descricao = driver.find_element(By.ID, 'desc_comida')
descricao.send_keys('Pão, Hambúrguer de 56g, Queijo, Presunto, Milho, Alface, Tomate e Maionese da Casa')
time.sleep(2)

## Preenchendo o preço
preco = driver.find_element(By.ID, 'preco_comida')
preco.send_keys('16.50')
time.sleep(2)

'''
driver.find_element(By.ID,'btn_salvar').click()
time.sleep(8)
print("Aguardando o Django processar e recarregar a página...")
'''

# --- PÁGINA GERENTE ---
driver.find_element(By.ID, 'btn_visualizar').click()
time.sleep(2)

# Guarda o identificador da aba atual (Gerente) antes de clicar
aba_gerente = driver.current_window_handle

# Clicará no link que abre em Nova Aba
driver.find_element(By.ID, 'visao_cliente').click()
time.sleep(3) 

# --- ALTERNANDO PARA A NOVA ABA (CLIENTE) ---
# Pega todas as abas abertas atualmente
todas_as_abas = driver.window_handles

# Loop para mudar o foco do Selenium para a aba que NÃO seja a do gerente
for aba in todas_as_abas:
    if aba != aba_gerente:
        driver.switch_to.window(aba)
        break

print("Foco do Selenium alterado para a aba do Cliente!")

# --- PÁGINA CLIENTE
driver.find_element(By.ID,'adc_pedido').click()
time.sleep(3)
driver.find_element(By.ID,'meuPedido').click()
time.sleep(3)


nome_input = driver.find_element(By.ID,'seu_nome')
nome_input.send_keys('Daniel Santos')
time.sleep(3)

driver.find_element(By.ID,'btn_enviarpedido').click()
time.sleep(5)

driver.close() # Fecha a aba do cliente
driver.switch_to.window(aba_gerente)
time.sleep(2)
#Ver os pedidos feito
driver.find_element(By.ID, 'gerente_pedidos').click()
time.sleep(6) #Para visualizar melhor

driver.quit()
