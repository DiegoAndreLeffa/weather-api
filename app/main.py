from fastapi import FastAPI

app = FastAPI(
    title="Weather API",
    description="API para consulta e armazenamento de dados climáticos.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }