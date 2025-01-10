# Projeto de Treinamento

## Objetivo

Este projeto foi desenvolvido com o objetivo de se familiarizar com o Django, aprender como o Celery funciona e como configurá-lo com o Redis. Tudo isso foi feito utilizando Docker para facilitar o ambiente de desenvolvimento.

## Tecnologias Utilizadas
- **Django**: Framework web para Python.
- **Celery**: Framework assíncrono para execução de tarefas em segundo plano.
- **Redis**: Armazenamento de dados em memória, utilizado como "broker" do Celery.
- **Docker**: Ferramenta para automação de containers, garantindo um ambiente de desenvolvimento isolado e consistente.

## Detalhes
Para armazenar os dados do projeto, foi usada a imagem do PostgreSQL para subir um container Docker.
O projeto é basicamente um sistema simples de uma loja onde temos algumas entidades que foram criadas a partir de uma modelagem:
- Cliente
- Produto
- ItemCarrinho
- Compra
- ItemCompra

## Subindo o Projeto Localmente

Para rodar o projeto localmente, siga os passos abaixo:

### 1. Clone o Repositório
Clone o repositório para o seu computador:
```bash
git clone https://github.com/adryelli-reis/projeto_trainee
cd projeto_trainee
```

### 2. Configuração do Docker
Antes de rodar o projeto, certifique-se de que você tem o Docker instalado. Caso não tenha, siga a documentação oficial do Docker para instalar: [Docker Docs](https://docs.docker.com/).
No diretório do projeto, você já deve ter um arquivo `docker-compose.yml` configurado. Verifique se ele contém a configuração para o Django, Celery, Redis e PostgreSQL (se necessário).

### 3. Construir e Subir os Containers Docker
No terminal, dentro do diretório do projeto, execute:
```bash
docker compose up --build # ou docker-compose
```
Isso vai construir as imagens necessárias e subir os containers do Django, Celery, Redis e PostgreSQL (se configurado no seu projeto).

### 4. Rodar as Migrations
Depois que os containers estiverem rodando, é hora de rodar as migrations para configurar o banco de dados:
```bash
docker compose exec web python manage.py migrate # ou docker-compose
```

### 5. Criar um Superusuário (Opcional)
Se precisar acessar o painel de administração do Django, crie um superusuário:
```bash
docker compose run web python manage.py createsuperuser # ou docker-compose
```

### 6. Popular o Banco de Dados
Existe um comando e um arquivo configurado para popular o banco de dados com alguns dados fictícios. Não é necessário, mas me ajudou no desenvolvimento e teste da API.
```bash
docker compose run web python manage.py popula_banco # ou docker-compose
```

### 7. Acessando o Projeto
Abra o navegador e acesse:
- **Django**: `http://localhost:8000/`
- **Administração do Django**: `http://localhost:8000/admin/` (precisa do superusuário)

### 8. Parando os Containers
Para parar os containers, execute:
```bash
docker compose down # ou docker-compose
```

## Rotas e Testes
Existe um Workspace privado no Postman que já está com todas as rotas de requisições criadas.

### Task async
Existe uma rota que trabalha com o task async do Celery para aplicar desconto a todos os produtos cadastrados:
```/produtos/aplicar_desconto```.

**Corpo da requisição**:
```json
{
    "percentual_desconto": <valor_inteiro>
}
```
Basicamente atualiza o campo `desconto` de todos os produtos que estão em estoque.

## Comandos (extra)

### Iniciar o container do Django
```bash
docker compose run --rm web django-admin startproject projeto_trainee .
```

### Criar o app no Django
```bash
docker compose run --rm web python manage.py startapp store
```

### Instalação manual
```bash
docker compose run web pip install -r requirements.txt
```

### Se necessário

Instalar o Celery e o Redis:
```bash
docker compose run --rm web pip install celery redis
```

### Rodar o Celery
```bash
docker compose run web celery -A projeto_trainee worker --loglevel=info
```

### Rodar o Django
```bash
docker compose run web python manage.py runserver 0.0.0.0:8000
```

### Criar as migrations
```bash
docker compose run web python manage.py makemigrations
```

### Aplicar as migrations e criar as tabelas no banco de dados
```bash
docker compose run web python manage.py migrate
```

### Popular o banco de dados
```bash
docker compose run web python manage.py popula_banco
```

### Acessar o shell do Django
```bash
docker compose run web python manage.py shell
```

### Verificar tabelas diretamente no PostgreSQL
```bash
docker compose exec db psql -U adry -d mydb
```
Lista as tabelas
```
\dt
```

### Subir tudo
```bash
docker compose up
```
