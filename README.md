# API Simples de Bolsa de Emprego

Esta aplicação é uma API desenvolvida em Django e Django REST Framework para um quadro de empregos. A API permite aos utilizadores autenticados publicar, procurar e gerir empregos, bem como criar e visualizar candidaturas a empregos.

---

## Passos para Executar a Aplicação

1. **Crie um Ambiente Virtual**

   - No diretório do projeto, crie um ambiente virtual:
     ```bash
     python -m venv venv
     ```
   - Ative o ambiente virtual:
     - **Windows**:
       ```bash
       venv\Scripts\activate
       ```
     - **Linux/Mac**:
       ```bash
       source venv/bin/activate
       ```

2. **Crie o arquivo `.env`**

   - Na raiz do projeto, crie um arquivo chamado `.env`.
   - Adicione as seguintes variáveis:
     ```env
     SECRET_KEY=sua_chave_secreta_aqui
     DEBUG=True
     JWT_SECRET_KEY=sua_chave_secreta_para_jwt
     DB_NAME=nome_do_banco
     DB_USER=usuario_do_banco
     DB_PASSWORD=senha_do_banco
     DB_HOST=localhost
     DB_PORT=3306
     ```

3. **Instale os Pacotes Necessários**

   - Certifique-se de estar com o ambiente virtual ativado.
   - Instale os pacotes listados no arquivo `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

4. **Configure e Migre o Banco de Dados**

   - Certifique-se de que o MySQL está configurado e a base de dados está acessível.
   - Execute os comandos para criar as tabelas no banco:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

5. **Criação de Superusuário**

   - Após migrar o banco de dados, crie um superutilizador para aceder ao painel de administração:
     ```bash
     python manage.py createsuperuser
     ```
   - Insira as informações solicitadas, como **nome de utilizador**, **email** e **password**.
   - Após a criação bem-sucedida, pode aceder ao painel de administração no URL padrão:
     ```url
     http://127.0.0.1:8000/admin/
     ```

6. **Execute a Aplicação**

   - No terminal, com o ambiente virtual ativado, execute o servidor:
     ```bash
     python manage.py runserver
     ```
   - A aplicação será iniciada no endereço padrão: `http://127.0.0.1:8000`.

---

## Endpoints Disponíveis

### **Autenticação**

#### 1. **Registrar Usuário**

- **URL**: `/auth/register_user`
- **Método**: `POST`
- **Descrição**: Registra um novo utilizador no sistema.
- **Cabeçalho**:

  ```json
  Content-Type: application/json
  ```

- **Body (JSON)**:

```json
{
  "first_name": "John",
  "other_names": "Doe",
  "email": "johndoe@example.com",
  "username": "johndoe",
  "password": "Password123!"
}
```

- **Resposta de Sucesso (201)**:

```json
{
  "success": true,
  "message": "User registered successfully!",
  "data": {
    "id": 1,
    "first_name": "John",
    "other_names": "Doe",
    "email": "johndoe@example.com",
    "username": "johndoe",
    "date_created": "2025-01-21 12:00:00"
  }
}
```

### 2. **Login**

- **URL**: `/auth/login`
- **Método**: `POST`
- **Descrição**: Autentica um utilizador e retorna tokens JWT.

- **Body (JSON)**:

```json
{
  "identifier": "johndoe@example.com",
  "password": "Password123!"
}
```

- **Resposta de Sucesso (200)**:

```json
{
  "success": true,
  "message": "Login successfully!",
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token"
}
```

### **Empregos**

### 1. **Listar Empregos**

- **URL**: `/jobs`
- **Método**: `GET`
- **Descrição**: Retorna uma lista de todos os empregos.

- **Resposta de Sucesso (200)**:

```json
{
  "success": true,
  "message": "Jobs found successfully!",
  "data": [
    {
      "id": 1,
      "title": "IT Support",
      "company": "Example",
      "location": "Remote",
      "description": "Provide IT support to employees.",
      "category": "Tech",
      "posted_by": {
        "id": 1,
        "full_name": "John Doe"
      },
      "date_created": "2025-01-21 12:00:00"
    }
  ]
}
```

### 2. **Criar um Emprego**

- **URL**: `/jobs`
- **Método**: `POST`
- **Descrição**: Cria uma nova publicação de emprego.

- **Body (JSON)**:

```json
{
  "title": "IT Support",
  "company": "Example",
  "location": "Remote",
  "description": "Provide IT support to employees.",
  "category": "Tech"
}
```

### 3. **Detalhes do Emprego**

- **URL**: `/jobs/{jobId}`
- **Método**: `GET, PUT, DELETE`
- **Descrição**: Visualiza, atualiza ou exclui um emprego específico.

### **Procurar Empregos**

#### 1. **Buscar Empregos**

- **URL**: `/search`
- **Método**: `GET`
- **Descrição**: Pesquisa empregos por título, empresa, localização ou palavras-chave.

- **Parâmetros de Consulta**:

  - `title`: Pesquisa por título do emprego.
  - `company`: Pesquisa por nome da empresa.
  - `location`: Pesquisa por localização do emprego.
  - `keywords`: Pesquisa por palavras-chave na descrição do emprego.

- **Exemplo de Requisição**:

  ```bash
  curl --location 'http://127.0.0.1:8000/search?title=developer&location=Remote' \
  --header 'Authorization: Bearer <access_token>'

  ```

- **Resposta de Sucesso (200)**:

```json
{
  "success": true,
  "message": "Jobs found successfully!",
  "data": [
    {
      "id": 1,
      "title": "Frontend Developer",
      "company": "TechCorp",
      "location": "Remote",
      "description": "Develop user interfaces for web applications.",
      "category": "Software Development",
      "posted_by": {
        "id": 1,
        "full_name": "John Doe"
      },
      "date_created": "2025-01-21 12:00:00"
    }
  ]
}
```

- **Resposta de Erro (404)**:

```json
{
  "success": false,
  "message": "No jobs found matching the search criteria."
}
```

### **Candidaturas**

### 1. **Criar uma Candidatura**

- **URL**: `/jobs/{jobId}/apply`
- **Método**: `POST`
- **Descrição**: Permite que um utilizador se candidate a um emprego.

- **Body (JSON)**:

```json
{
  "cover_letter": "I am very interested in this position."
}
```

- **Resposta de Sucesso (201)**:

```json
{
  "success": true,
  "message": "Application submitted successfully!",
  "data": {
    "id": 1,
    "job": {
      "title": "IT Support",
      "company": "Example",
      "location": "Remote"
    },
    "applicant": {
      "id": 1,
      "full_name": "John Doe"
    },
    "cover_letter": "I am very interested in this position.",
    "date_created": "2025-01-21 12:00:00"
  }
}
```

### 2. **Listar Candidaturas do Emprego**

- **URL**: `/jobs/{jobId}/applications/owner`
- **Método**: `POST`
- **Descrição**: Lista todas as candidaturas de um emprego para o criador do emprego.

- **Resposta de Sucesso (200)**:

```json
{
  "success": true,
  "message": "Job applications found successfully!",
  "data": [
    {
      "id": 1,
      "applicant": {
        "id": 2,
        "full_name": "Jane Doe"
      },
      "cover_letter": "I am very interested in this position.",
      "date_created": "2025-01-21 12:00:00"
    }
  ]
}
```

- **Resposta de Erro (403)**:

```json
{
  "success": false,
  "message": "You are not authorized to view applications for this job."
}
```

- **Resposta de Erro (404)**:

```json
{ 
  "success": false, 
  "message": "Job doesn't have applications yet!" 
}
```

### 3. **Detalhes de uma Candidatura**

- **URL**: `/applications/{applicationId}`
- **Método**: `GET`
- **Descrição**: Visualiza detalhes de uma candidatura específica.

- **Resposta de Sucesso (200)**:

```json
{
  "success": true,
  "message": "Job application found successfully!",
  "data": {
    "id": 1,
    "job": {
      "title": "IT Support",
      "company": "Updated Company 3",
      "location": "Updated Location"
    },
    "applicant": { "id": 1, "full_name": "John Doe" },
    "cover_letter": "Mas",
    "date_created": "2025-01-21 12:16:53"
  }
}
```

- **Resposta de Erro (404)**:

```json
{
  "success": false,
  "message": "Job application not found!"
}
```

## Estrutura do Projeto

# Estrutura do Projeto

job_board/
├── job_board/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── jobs/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tests.py
│   └── urls.py
├── manage.py
├── requirements.txt
.env
venv/
README.md



## Demonstração

- **Local**: `http://127.0.0.1:8000/`
- **Hospedado**: 
