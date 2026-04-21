import random

def predict_volatility_service(ticker: str) -> dict:
    """
    Função principal do serviço. 
    No futuro, o Cientista de Dados vai apagar este Mock e colocar a lógica real:
    1. Baixar yfinance
    2. Calcular features
    3. Rodar model.predict()
    """
    
    # --- INÍCIO DO MOCK (Dados Falsos para o Frontend trabalhar) ---
    
    # Simula a volatilidade atual entre 15% e 35%
    current_vol = random.uniform(0.15, 0.35)
    
    # Simula a volatilidade futura 
    pred_vol = current_vol * random.uniform(0.9, 1.2)
    
    # Regra de negócio simples para classificar o risco
    if pred_vol < 0.20:
        risk = "BAIXO"
    elif pred_vol < 0.30:
        risk = "NORMAL"
    else:
        risk = "ALTO"

    # --- FIM DO MOCK ---

    return {
        "ticker": ticker.upper(),
        "current_volatility": round(current_vol, 4),
        "predicted_volatility": round(pred_vol, 4),
        "risk_status": risk
    }