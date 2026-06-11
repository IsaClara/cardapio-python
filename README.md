# 🍢 Sistema de Gerenciamento de Pedidos

Projeto desenvolvido para solucionar problemas de organização e atendimento em pequenos comércios de rua, automatizando o fluxo de pedidos de forma visual e intuitiva.

🌐 **Acesse o projeto em produção:** [[Gerenciamento de Pedidos](https://cardapio-python.onrender.com/login/)]


## 🔴 O Problema
Uma pessoa que vende espetinhos na rua enfrenta grandes dificuldades para gerenciar as vendas nos horários de pico. Muitos clientes a cercam e fazem pedidos verbais ao mesmo tempo, gerando:
* Confusão na ordem de chegada dos pedidos.
* Erros nas entregas e esquecimento de acompanhamentos.
* Sobrecarga para a empreendedora, que precisa assar a carne e memorizar a fila simultaneamente.
* Clientes desistem devido à confusão ou demora.

## 🟢 A Solução
Criamos uma plataforma web focada em organização visual e criação de uma fila virtual por ordem de chegada:

* **Para o Cliente:** Acessa o site (via QR Code ou link), visualiza o cardápio digital atualizado e faz o seu pedido de forma autónoma.
* **Para a Proprietária (Painel Administrativo):** Um painel simples onde ela pode gerir categorias, produtos e preços. Inclui uma função para visualizar o site idêntico ao cliente (garantindo o controlo de qualidade do cardápio) e um **chatbot integrado** para auxiliá-la na administração do sistema.


## 📈 Resultados Obtidos
Com a implementação do sistema e os testes realizados, pode alcançar os seguintes resultados:
* **Fila Organizada:** Eliminação total do tumulto verbal ao redor da barraca, substituído por uma fila digital automatizada por ordem de chegada.
* **Otimização do Tempo:** A proprietária pode a focar exclusivamente no preparo dos alimentos, sem a necessidade de parar para anotar ou memorizar pedidos.
* **Redução de Erros:** O painel administrativo claro e o carrinho inteligente reduziram a zero a troca de pedidos ou o esquecimento de acompanhamentos.
* **Autonomia na Gestão:** A comerciante pode atualizar preços e categorias de forma independente, validando as alterações em tempo real através do modo de visualização do cliente.
* **Confiabilidade da Aplicação:** Graças aos testes automatizados rigorosos, o sistema se mostrou estável para rodar em produção sem falhas críticas nos fluxos principais.


## 🛠️ Dificuldades no Projeto (Desafios Técnicos)
Durante o desenvolvimento do sistema, o grupo enfrentou e superou os seguintes desafios de lógica e implementação:

1. **Implementação do Chatbot:** Configurar a lógica do assistente virtual para que ele responda corretamente e forneça ajuda real na administração, sem poluir a interface.
2. **Lógica de Quantidade no Carrinho:** Desenvolver a inteligência do sistema para somar a quantidade do mesmo produto quando clicado mais de uma vez, evitando a duplicação desnecessária de linhas na lista.
3. **Filtro de Alimentos:** Criar um sistema de filtragem eficiente para que os utilizadores encontrem rapidamente os espetinhos e acompanhamentos desejados.
4. **Gerenciamento da Lista de Pedidos:** Estruturar o fluxo de dados em tempo real para receber, ordenar e exibir os pedidos de forma limpa no painel da proprietária.
5. **Navegação e Rotas:** Fazer a conexão correta entre as diferentes páginas (Home, Cardápio, Painel Administrativo, Carrinho) garantindo a fluidez da aplicação.
6. **Criação de Categorias e Comidas (CRUD):** Implementar as funções de base de dados/estado para cadastrar, editar e excluir dinamicamente as categorias (ex: "Bebidas", "Espetinhos") e os produtos.

---

## 🚀 Tecnologias Utilizadas
* **Front-end:** HTML5, CSS3, JavaScript
* **Back-end & Banco de Dados:** Python, Django
* **Testes Automatizados:** Selenium
* **Deploy & Hospedagem:** Render