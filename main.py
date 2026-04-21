from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import do ramal
from app.api.endpoints import router as api_router

# Cria a instância oficial do app web
app = FastAPI(
    title="Volatility Predictor API",
    description="API para previsão de volatilidade da Diretoria de Data Science.",
    version="1.0.0"
)

# --- CONFIGURAÇÃO DE CORS (Crucial!) ---
# Quando o cara do Frontend for rodar a tela no computador dele, a tela vai abrir
# em uma porta (ex: localhost:3000) e nossa API está em outra (localhost:8000).
# O navegador bloqueia isso por segurança. O CORS avisa: "Pode confiar, eu deixo ele conectar".
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # em breve colocar o site oficial aqui. Por enquanto liberamos tudo para testes.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# plugando o ramal no app
app.include_router(api_router)
