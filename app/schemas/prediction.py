from pydantic import BaseModel, Field

# Aqui definimos o formato exato da RESPOSTA que nossa API vai devolver
class PredictionResponse(BaseModel):
    # Field(...) significa que este campo é obrigatório. 
    # O 'example' e o 'description' são o que vão fazer o Swagger UI ficar lindo e autoexplicativo.
    ticker: str = Field(..., example="PETR4.SA", description="O código do ativo financeiro")
    
    current_volatility: float = Field(..., example=0.2541, description="Volatilidade anualizada atual")
    
    predicted_volatility: float = Field(..., example=0.2815, description="Volatilidade prevista para os próximos dias")
    
    risk_status: str = Field(..., example="ALTO", description="Classificação de risco da operação (BAIXO, NORMAL, ALTO)")