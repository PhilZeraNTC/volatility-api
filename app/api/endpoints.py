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
    """
    Recebe um Ticker (ex: PETR4.SA), chama o serviço de Machine Learning
    e devolve a previsão formatada.
    """
    try:
        # Chamando o service
        result = predictor.get_prediction_data(ticker)
        return result
        
    except Exception as e:
        # Se algo der errado lá no service, captura o erro aqui
        raise HTTPException(status_code=400, detail=str(e))