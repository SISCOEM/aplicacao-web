
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
source venv/bin/activate -> acessar a pasta venv/bin/ para executar o comando
```

## 3. Instalar as Dependências

Após ativar o ambiente virtual, instale os pacotes necessários usando `pip`:

```bash
pip install -r requirements.txt
```

## 4. Configuração do Banco de Dados

Crie o banco de dados e o adicione no arquivo .env

```bash
DB_NAME={nome do banco de dados}
DB_USERNAME={nome de usuário}
DB_PASS={senha de usuário}
DB_PORT=3306
DB_HOST=localhost
```

#### 4.1 Acesse o terminal django do banco de dados

```bash
python manage.py dbshell
```

#### 4.2 Execute os comandos que estão no arquivo `sicomb/content_type.sql`

#### 4.3 Saia do terminal

Após executar os comandos, execute:

```bash
exit
```

#### 4.4 Após sair do terminal

Execute o comando:

```bash
python manage.py migrate --fake contenttypes
```

Em seguida, execute:

```bash
python manage.py migrate
```

## 5. Crie um superusuário

Execute o comando:

```bash
python manage.py createsuperuser
```

Em seguida, siga os passos informados no terminal.

## 6. Executar o Servidor de Desenvolvimento

Por fim, inicie o servidor de desenvolvimento do Django com:

```bash
python manage.py runserver 0.0.0.0:8000
```

ou

```bash
python manage.py runserver
```

Obs.: O comando com 0.0.0.0:8000 abre a aplicação para rede. Julgue se é necessário ou não.

Acesse `http://127.0.0.1:8000/` no seu navegador para visualizar a aplicação.
