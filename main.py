import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# import do ramal
from app.api.endpoints import router as api_router

# Cria a instância oficial do app web
app = FastAPI(
    title="Volatility Predictor API",
    description="API para previsão de volatilidade da Diretoria de Data Science.",
    version="1.0.0"
)


# --- CONFIGURAÇÃO DE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # em breve colocar o site oficial aqui. Por enquanto liberamos tudo para testes.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# plugando o ramal no app
app.include_router(api_router, prefix="/api")


public_path = "front/src/dist"

#verifica e monta os arquivos estaticos do front end
if os.path.exists(os.path.join(public_path, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(public_path, "assets")), name="assets")

@app.get("/{catchall:path}")
async def serve_frontend(catchall: str):
    # Se o arquivo existir na pasta dist (ex: favicon), retorna ele
    file_path = os.path.join(public_path, catchall)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # Caso contrário, retorna o index.html (essencial para o Vue Router funcionar)
    return FileResponse(os.path.join(public_path, "index.html"))
