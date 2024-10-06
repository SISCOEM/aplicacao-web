
# Guia de Configuração da aplicação web

Siga estes passos para clonar o repositório, configurar um ambiente virtual e instalar as dependências da aplicação web do SISCOEM.

## 1. Clonar o Repositório

Comece clonando o repositório a partir do GitHub.

```bash
git clone https://github.com/SISCOEM/aplicacao-web.git
cd aplicacao-web
```

## 2. Criar e Ativar um Ambiente Virtual

Para isolar as dependências do projeto, recomenda-se o uso de um ambiente virtual.

### No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### No macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate -> acessar a pasta venb/bin/ para exeutar o comando
```

## 3. Instalar as Dependências

Após ativar o ambiente virtual, instale os pacotes necessários usando `pip`:

```bash
pip install -r requirements.txt
no diretorio SIScomb utilizar pip3
```


## 4. Aplicar as Migrações

Antes de executar a aplicação, aplique as migrações para configurar o esquema do banco de dados:

```bash
python manage.py migrate
```

Siga as instruções para configurar as credenciais do superusuário.

## 5. Executar o Servidor de Desenvolvimento

Por fim, inicie o servidor de desenvolvimento do Django:

```bash
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/` no seu navegador para visualizar a aplicação.

