from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

# Templates
templates = Jinja2Templates(directory="app/templates")

# App FastAPI
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Renderiza o dashboard inicial."""
    # Dados estáticos de exemplo
    opportunities = [
        {"token": "ADA", "spread": 4.0, "fees": 0.5, "volume": "R$ 5.000"},
        {"token": "BTC", "spread": 2.5, "fees": 0.7, "volume": "R$ 15.000"},
    ]
    return templates.TemplateResponse("dashboard.html", {"request": request, "opportunities": opportunities})
