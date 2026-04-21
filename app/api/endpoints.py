from fastapi import APIRouter, HTTPException
from app.schemas.prediction import PredictionResponse
from app.services.model_service import predict_volatility_service

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
        # Chamamos o Motor que você criou na etapa anterior
        result = predict_volatility_service(ticker)
        return result
        
    except Exception as e:
        # Se algo der errado lá no motor, nós capturamos o erro aqui
        # e devolvemos um Erro 400 (Bad Request) bonitinho para o usuário,
        # em vez de deixar o servidor "crashar".
        raise HTTPException(status_code=400, detail=str(e))