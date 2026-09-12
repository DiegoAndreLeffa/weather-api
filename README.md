# Weather API

API REST desenvolvida em Python para consulta e armazenamento de dados climáticos utilizando a API pública do OpenWeather.

Os dados consultados são transformados e persistidos em um banco de dados PostgreSQL, permitindo posteriormente consultar o histórico através da própria API.

O projeto foi desenvolvido como parte de uma avaliação técnica, com foco em organização de código, integração com API externa, persistência de dados, criação de endpoints REST, testes automatizados e execução utilizando Docker.

## Tecnologias utilizadas

* **Python 3.13**
* **FastAPI** — criação da API REST e documentação OpenAPI
* **SQLAlchemy** — ORM para comunicação com o banco de dados
* **PostgreSQL** — banco de dados relacional
* **Psycopg** — driver PostgreSQL para Python
* **HTTPX** — comunicação assíncrona com a API externa
* **Pydantic Settings** — gerenciamento de configurações e variáveis de ambiente
* **Pytest** — testes automatizados
* **Docker**
* **Docker Compose**
* **Git**

## Funcionalidades

* Consulta de cidades através da API de Geocoding do OpenWeather.
* Consulta das condições climáticas atuais.
* Transformação e enriquecimento dos dados recebidos da API externa.
* Persistência dos dados no PostgreSQL.
* Consulta do histórico de dados armazenados.
* Consulta de um registro específico por ID.
* Filtro do histórico por cidade.
* Limite configurável para resultados.
* Validação rigorosa dos parâmetros recebidos.
* Tratamento de erros e exceções da API externa.
* Health check da aplicação e da conexão com o banco de dados.
* Documentação interativa através do Swagger e ReDoc.
* Testes automatizados com isolamento completo (mocks e SQLite em memória).
* Execução completa e reprodutível através de Docker Compose.

## Estrutura do projeto

```text
weather-api/
│
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── init_db.py
│   │
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── weather.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── weather.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── weather.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── weather_service.py
│   │
│   ├── __init__.py
│   └── main.py
│
├── tests/
│   ├── __init__.py
│   ├── test_weather_api.py
│   └── test_weather_service.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Pré-requisitos

Para executar o projeto localmente, é necessário ter instalado:

* Python 3.13 ou superior
* PostgreSQL (caso execute fora do Docker)
* Uma chave de API do OpenWeather

Para executar utilizando Docker:

* Docker Desktop / Docker Engine com Docker Compose

## Configuração das variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto utilizando o arquivo `.env.example` como referência:

```env
OPENWEATHER_API_KEY=your_openweather_api_key_here
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/weather_db
```

### Variáveis

| Variável              | Descrição                                                 |
| --------------------- | --------------------------------------------------------- |
| `OPENWEATHER_API_KEY` | Chave utilizada para autenticação nas APIs do OpenWeather |
| `DATABASE_URL`        | String de conexão com o PostgreSQL                        |

> O arquivo `.env` não deve ser versionado no Git, pois contém informações de configuração e credenciais.

## Executando com Docker (Recomendado)

O projeto possui um `Dockerfile` e um `docker-compose.yml` responsáveis por orquestrar a API juntamente com o banco PostgreSQL.

### 1. Configure o `.env`

Na raiz do projeto, crie o arquivo `.env` contendo a sua chave da OpenWeather:

```env
OPENWEATHER_API_KEY=sua_chave_aqui
```

### 2. Suba os containers

```bash
docker compose up --build
```

O Docker Compose irá:

1. Criar e iniciar o container do PostgreSQL 17.
2. Criar automaticamente o banco de dados `weather_db`.
3. Aguardar o banco estar 100% pronto através do `healthcheck`.
4. Construir a imagem da API e iniciar a aplicação na porta `8000`.
5. Criar automaticamente as tabelas necessárias no banco através do ciclo de vida (*lifespan*) da aplicação.

A API ficará disponível em:

```text
http://localhost:8000
```

Para parar os containers:

```bash
docker compose down
```

Para parar os containers e remover também os volumes persistidos do banco:

```bash
docker compose down -v
```

## Executando localmente (Sem Docker)

### 1. Clone o repositório

```bash
git clone https://github.com/DiegoAndreLeffa/weather-api.git
cd weather-api
```

### 2. Crie e ative um ambiente virtual

No Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados e variáveis

Crie uma base PostgreSQL chamada `weather_db` e configure o arquivo `.env` com as suas credenciais locais e sua chave da API.

### 5. Execute a aplicação

```bash
fastapi dev app/main.py
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

## Documentação da API

Após iniciar a aplicação, a documentação interativa com Swagger pode ser acessada em:

```text
http://localhost:8000/docs
```

A documentação alternativa com ReDoc está disponível em:

```text
http://localhost:8000/redoc
```

## Endpoints

### Health Check

Verifica a saúde da API e a conectividade com o banco de dados.

```http
GET /health
```

Exemplo de resposta (Status `200 OK`):

```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

### Buscar clima e armazenar

Consulta as coordenadas da cidade informada na API de Geocoding da OpenWeather, obtém os dados meteorológicos atuais, realiza a transformação e persiste o registro no banco de dados.

Seguindo as boas práticas RESTful para criação de recursos, o endpoint principal é um `POST` com retorno `201 Created`:

```http
POST /api/v1/weather/{city}
```

> *Nota: Por conveniência para testes rápidos pelo navegador, o endpoint também responde via `GET /api/v1/weather/{city}` com o mesmo comportamento.*

Exemplo:

```http
POST /api/v1/weather/Florianopolis
```

Exemplo de resposta (Status `201 Created`):

```json
{
  "id": 1,
  "city": "Florianópolis",
  "country": "BR",
  "latitude": -27.5968,
  "longitude": -48.5519,
  "temperature": 19.48,
  "feels_like": 19.86,
  "humidity": 91,
  "pressure": 1010,
  "weather": "Clouds",
  "description": "nublado",
  "wind_speed": 4.12,
  "recorded_at": "2026-09-10T21:47:41.900011"
}
```

---

### Consultar histórico armazenado

Retorna a lista dos registros climáticos persistidos no banco de dados, ordenados dos mais recentes para os mais antigos.

```http
GET /api/v1/weather
```

Parâmetros de consulta (Query Parameters):

| Parâmetro | Tipo    | Obrigatório | Padrão | Descrição                                        |
| --------- | ------- | ----------- | ------ | ------------------------------------------------ |
| `city`    | string  | Não         | -      | Filtra os registros contendo o nome da cidade    |
| `limit`   | integer | Não         | `10`   | Quantidade máxima de registros retornados (1-100)|

Exemplo:

```http
GET /api/v1/weather?city=Florianopolis&limit=5
```

---

### Consultar registro por ID

Retorna um registro climático específico armazenado no banco pelo seu identificador primário.

```http
GET /api/v1/weather/id/{id}
```

Exemplo:

```http
GET /api/v1/weather/id/1
```

Caso o registro não exista, a API retorna Status `404 Not Found`:

```json
{
  "detail": "Registro não encontrado."
}
```

## Fluxo da aplicação

Quando uma extração é solicitada, o fluxo de dados executado é:

```text
Cliente / Swagger
   │
   ▼
FastAPI Router
   │
   ▼
OpenWeather Geocoding API ──► Obtém latitude, longitude e nome padronizado
   │
   ▼
OpenWeather Current API   ──► Obtém temperatura, umidade, vento, etc.
   │
   ▼
Transformação & Modelagem (Pydantic / SQLAlchemy)
   │
   ▼
Persistência no PostgreSQL
   │
   ▼
Resposta HTTP 201 com o recurso salvo
```

## Banco de dados

Os dados são armazenados na tabela `weather_records`:

| Campo         | Tipo             | Descrição                 |
| ------------- | ---------------- | ------------------------- |
| `id`          | Integer (PK, AI) | Identificador do registro |
| `city`        | String(100)      | Nome da cidade            |
| `country`     | String(10)       | Código do país            |
| `latitude`    | Float            | Latitude geográfica       |
| `longitude`   | Float            | Longitude geográfica      |
| `temperature` | Float            | Temperatura em °C         |
| `feels_like`  | Float            | Sensação térmica em °C    |
| `humidity`    | Integer          | Umidade relativa (%)      |
| `pressure`    | Integer          | Pressão atmosférica (hPa) |
| `weather`     | String(50)       | Categoria climática       |
| `description` | String(100)      | Descrição em português    |
| `wind_speed`  | Float            | Velocidade do vento (m/s) |
| `recorded_at` | DateTime         | Momento da persistência   |

## Testes

Os testes automatizados utilizam `pytest` e foram construídos com foco em **total isolamento e reprodutibilidade**:

* **Sem dependência externa:** Todas as requisições HTTP ao OpenWeather são mockadas, garantindo que os testes rodem rápido e não consumam sua cota de API.
* **Sem dependência de banco de dados ativo:** Os testes de integração utilizam um banco **SQLite em memória**, permitindo rodar a suíte completa sem precisar ter o PostgreSQL instalado ou em execução.

Para executar todos os testes:

```bash
pytest
```

A suíte cobre:

* Validação de parâmetros inválidos da API (Status 422);
* Tratamento de busca por ID inexistente (Status 404);
* Sucesso e parsing da consulta de coordenadas (Geocoding);
* Tratamento de erro para cidades não encontradas na API externa;
* Fluxo completo de consulta, enriquecimento e persistência no serviço de clima.

## Licença

Projeto desenvolvido para fins de avaliação técnica e demonstração prática de integração de APIs, persistência relacional, containerização com Docker e boas práticas de desenvolvimento em Python.