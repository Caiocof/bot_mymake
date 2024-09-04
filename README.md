# Telegram Stock Bot

Este projeto implementa um sistema básico de estoque utilizando um bot do Telegram. O bot permite cadastrar produtos, registrar vendas, listar o estoque, e verificar vencimentos de vendas realizadas em notas fiscais. O backend será desenvolvido em Python com integração ao banco de dados MySQL.

## Funcionalidades

1. **Cadastrar Produto:**
   - Solicitar informações: `nome do produto`, `quantidade`, `valor de compra`, `valor de venda`.
   - Registrar os dados no banco de dados MySQL.

2. **Registrar Vendas:**
   - Solicitar informações: `código do produto (id)`, `quantidade`, `forma de pagamento` (cartão, dinheiro, pix ou nota).
   - Se a forma de pagamento for "nota", solicitar `nome da pessoa` e `data de vencimento`.
   - Registrar a venda no banco de dados MySQL.

3. **Listar Estoque:**
   - Listar produtos com `quantidade` maior que 0.
   - Exibir as informações: `código do produto (id)`, `nome do produto`, `quantidade`, `valor de venda`.

4. **Verificar Vencimentos do Dia:**
   - Listar vendas com pagamento em "nota" e vencimento nos próximos dois dias (incluindo a data atual).

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **MySQL**: Banco de dados relacional para armazenar as informações.
- **Python-telegram-bot**: Biblioteca para integração com o Telegram.
- **SQLAlchemy ou pymysql**: Biblioteca para interação com o MySQL.

## Passos para Implementação

### 1. Configuração Inicial

- [ ] Criar o bot no Telegram usando o `BotFather` e obter o token de acesso.
- [ ] Configurar o ambiente de desenvolvimento Python.
  - [ ] Criar um ambiente virtual (`venv`).
  - [ ] Instalar as dependências: `python-telegram-bot`, `SQLAlchemy` ou `pymysql`, `python-dotenv`.
  - [ ] Configurar um arquivo `.env` para armazenar o token do bot e credenciais do MySQL.

### 2. Criar o Banco de Dados

- [ ] Definir e criar o banco de dados MySQL.
  - [ ] Criar tabelas para `produtos`, `vendas`, e `vencimentos`.

### 3. Implementar Funcionalidades

#### 3.1. Cadastrar Produto

- [ ] Implementar o comando para cadastrar um novo produto.
- [ ] Solicitar as informações necessárias e validar a entrada.
- [ ] Inserir os dados no banco de dados MySQL.

#### 3.2. Registrar Vendas

- [ ] Implementar o comando para registrar uma nova venda.
- [ ] Solicitar as informações necessárias e validar a entrada.
- [ ] Se a forma de pagamento for "nota", solicitar informações adicionais.
- [ ] Inserir os dados da venda no banco de dados MySQL.

#### 3.3. Listar Estoque

- [ ] Implementar o comando para listar o estoque.
- [ ] Consultar o banco de dados para obter produtos com quantidade maior que 0.
- [ ] Exibir os dados em formato de tabela.

#### 3.4. Verificar Vencimentos do Dia

- [ ] Implementar o comando para verificar os vencimentos do dia.
- [ ] Consultar o banco de dados para encontrar vencimentos nos próximos dois dias.
- [ ] Exibir as informações das vendas que atendem aos critérios.

### 4. Melhorias Futuras

- [ ] Adicionar validações adicionais para os dados inseridos.
- [ ] Implementar geração de relatórios.
- [ ] Adicionar funcionalidade de backup automático.

## Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/telegram-stock-bot.git
   cd telegram-stock-bot
   ```

2. Crie um ambiente virtual e instale as dependências:
    ```bash
   python3 -m venv venv 
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente no arquivo .env. 

4. Execute o bot:
    ```bash
   python main.py
    ```  
