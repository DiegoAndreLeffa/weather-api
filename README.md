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
* **HTTPX** — comunicação com a API externa
* **Pydantic Settings** — gerenciamento de configurações e variáveis de ambiente
* **Pytest** — testes automatizados
* **Docker**
* **Docker Compose**
* **Git**

## Funcionalidades

* Consulta de cidades através da API de Geocoding do OpenWeather.
* Consulta das condições climáticas atuais.
* Transformação dos dados recebidos da API externa.
* Persistência dos dados no PostgreSQL.
* Consulta do histórico de dados armazenados.
* Consulta de um registro específico por ID.
* Filtro do histórico por cidade.
* Limite configurável para resultados.
* Validação dos parâmetros recebidos.
* Tratamento de erros da API externa.
* Health check da aplicação e do banco de dados.
* Documentação interativa através do Swagger.
* Testes automatizados.
* Execução completa através de Docker Compose.

## Estrutura do projeto

```text
weather-api/
│
├── app/
│   ├── core/
│   │   └── config.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── init_db.py
│   │
│   ├── exceptions/
│   │   └── weather.py
│   │
│   ├── models/
│   │   └── weather.py
│   │
│   ├── schemas/
│   │   └── weather.py
│   │
│   ├── services/
│   │   └── weather_service.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_weather_api.py
│   └── test_weather_service.py
│
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
* PostgreSQL
* Uma chave de API do OpenWeather

Para executar utilizando Docker:

* Docker Desktop

## Configuração das variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto.

Utilize o arquivo `.env.example` como referência:

```env
OPENWEATHER_API_KEY=your_openweather_api_key_here
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/weather_db
```

### Variáveis

| Variável              | Descrição                                                 |
| --------------------- | --------------------------------------------------------- |
| `OPENWEATHER_API_KEY` | Chave utilizada para autenticação nas APIs do OpenWeather |
| `DATABASE_URL`        | String de conexão com o PostgreSQL                        |

> O arquivo `.env` não deve ser versionado, pois contém informações de configuração e credenciais.

## Executando localmente

### 1. Clone o repositório

```bash
git clone https://github.com/DiegoAndreLeffa/weather-api.git
cd weather-api
```

### 2. Crie um ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Crie um banco PostgreSQL chamado:

```text
weather_db
```

Depois configure a variável `DATABASE_URL` no arquivo `.env`.

Exemplo:

```env
DATABASE_URL=postgresql+psycopg://postgres:sua_senha@localhost:5432/weather_db
```

### 5. Configure a chave do OpenWeather

No arquivo `.env`:

```env
OPENWEATHER_API_KEY=sua_chave_aqui
```

### 6. Execute a aplicação

```bash
fastapi dev app/main.py
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

## Executando com Docker

O projeto possui um `Dockerfile` para a aplicação e um `docker-compose.yml` responsável por executar a API juntamente com o PostgreSQL.

### 1. Configure o `.env`

Na raiz do projeto, crie um arquivo `.env` contendo:

```env
OPENWEATHER_API_KEY=sua_chave_aqui
```

### 2. Suba os containers

```bash
docker compose up --build
```

O Docker Compose irá:

1. Criar o container do PostgreSQL.
2. Criar o banco `weather_db`.
3. Aguardar o banco estar disponível através do health check.
4. Criar a imagem da API.
5. Iniciar a aplicação.
6. Conectar a API ao PostgreSQL através da rede interna do Docker.

A API ficará disponível em:

```text
http://localhost:8000
```

Para parar os containers:

```bash
docker compose down
```

Para parar os containers e remover também os volumes do banco:

```bash
docker compose down -v
```

> O comando recomendado para executar o projeto completo em Docker é `docker compose up --build`. O container da API depende das configurações e da rede criadas pelo Docker Compose.

## Documentação da API

Após iniciar a aplicação, a documentação interativa do Swagger pode ser acessada em:

```text
http://localhost:8000/docs
```

Também é possível acessar a documentação alternativa através do ReDoc:

```text
http://localhost:8000/redoc
```

## Endpoints

### Health Check

Verifica se a API está funcionando e se consegue estabelecer conexão com o banco de dados.

```http
GET /health
```

Exemplo de resposta:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Buscar clima e armazenar

Consulta uma cidade no OpenWeather, obtém os dados climáticos atuais, transforma os dados necessários e salva o resultado no PostgreSQL.

```http
GET /api/v1/weather/{city}
```

Exemplo:

```http
GET /api/v1/weather/Florianopolis
```

Exemplo de resposta:

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

O `id` retornado corresponde ao registro criado no banco de dados.

### Consultar histórico

Retorna os registros climáticos armazenados no PostgreSQL.

```http
GET /api/v1/weather
```

É possível utilizar os seguintes parâmetros:

| Parâmetro | Tipo    | Obrigatório | Descrição                                 |
| --------- | ------- | ----------- | ----------------------------------------- |
| `city`    | string  | Não         | Filtra os registros por cidade            |
| `limit`   | integer | Não         | Quantidade máxima de registros retornados |

O `limit` possui valor padrão de `10` e aceita valores entre `1` e `100`.

Exemplo:

```http
GET /api/v1/weather?city=Florianopolis&limit=5
```

### Consultar registro por ID

Retorna um registro específico armazenado no banco.

```http
GET /api/v1/weather/id/{id}
```

Exemplo:

```http
GET /api/v1/weather/id/1
```

Caso o registro não exista, a API retorna:

```http
404 Not Found
```

## Fluxo da aplicação

Quando uma cidade é consultada através do endpoint de busca, o fluxo principal é:

```text
Cliente
   │
   ▼
FastAPI
   │
   ▼
Geocoding API
   │
   ├── latitude
   ├── longitude
   └── informações da cidade
   │
   ▼
Current Weather API
   │
   ▼
Transformação dos dados
   │
   ▼
PostgreSQL
   │
   ▼
Resposta da API
```

A aplicação utiliza o serviço de Geocoding do OpenWeather para obter as coordenadas da cidade e, em seguida, utiliza essas coordenadas para consultar as condições climáticas atuais.

## Banco de dados

Os dados são armazenados na tabela:

```text
weather_records
```

Principais campos:

| Campo         | Tipo     | Descrição                 |
| ------------- | -------- | ------------------------- |
| `id`          | Integer  | Identificador do registro |
| `city`        | String   | Nome da cidade            |
| `country`     | String   | Código do país            |
| `latitude`    | Float    | Latitude                  |
| `longitude`   | Float    | Longitude                 |
| `temperature` | Float    | Temperatura atual         |
| `feels_like`  | Float    | Sensação térmica          |
| `humidity`    | Integer  | Umidade                   |
| `pressure`    | Integer  | Pressão atmosférica       |
| `weather`     | String   | Condição climática        |
| `description` | String   | Descrição da condição     |
| `wind_speed`  | Float    | Velocidade do vento       |
| `recorded_at` | DateTime | Data e hora do registro   |

## Testes

Os testes automatizados utilizam `pytest`.

Para executar:

```bash
pytest
```

Atualmente, o projeto possui **5 testes automatizados**, cobrindo:

* validação dos parâmetros da API;
* consulta de coordenadas de uma cidade;
* tratamento de cidade não encontrada;
* consulta, transformação e persistência dos dados climáticos;
* tratamento de registro não encontrado.

As chamadas ao OpenWeather utilizadas nos testes são simuladas através de mocks, evitando dependência do serviço externo durante a execução dos testes.

## Segurança e configuração

A chave da API do OpenWeather é carregada através de variável de ambiente e não fica diretamente no código-fonte.

O arquivo `.env` está incluído no `.gitignore` para evitar o versionamento de credenciais.

O projeto disponibiliza o arquivo `.env.example` contendo apenas a estrutura necessária para configuração.

## Possíveis melhorias futuras

Algumas melhorias que poderiam ser implementadas em uma evolução do projeto:

* adicionar paginação ao histórico;
* adicionar filtros por intervalo de datas;
* utilizar migrations com Alembic;
* adicionar autenticação à API;
* adicionar cache para reduzir chamadas à API externa;
* adicionar testes de integração com banco de dados;
* adicionar CI/CD para execução automática dos testes;
* adicionar observabilidade e métricas da aplicação.

## Repositório

O código-fonte completo do projeto está disponível no GitHub:

https://github.com/DiegoAndreLeffa/weather-api

## Licença

Este projeto foi desenvolvido para fins de avaliação técnica e demonstração de conhecimentos em desenvolvimento de APIs, integração com serviços externos, persistência de dados e containerização.
