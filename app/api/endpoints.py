from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.schemas.prediction import PredictionResponse
from app.services.model_service import predictor

# O APIRouter é como um "mini-aplicativo" que gerencia um grupo de rotas.
# Isso mantém o projeto organizado quando ele cresce.
router = APIRouter()

# Aqui definimos o método (GET), a URL (/predict/{ticker}) e o Contrato de saída (response_model)
@router.get("/predict/{ticker}", response_model=PredictionResponse)
async def get_prediction(ticker: str):
    try:
        return predictor.get_prediction_data(ticker)
    except ValueError as e:
        # Isso faz o Swagger mostrar o erro em vermelho e não gerar o card vazio
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno no servidor de ML")