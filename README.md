# 📈 Volatility Predictor - Liga de Mercado Financeiro UTFPR

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.104-009688?style=for-the-badge&logo=fastapi)
![LightGBM](https://img.shields.io/badge/LightGBM-4.1.0-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

Este repositório contém a fundação de uma ferramenta de **Data Science aplicada ao Mercado Financeiro**, focada na previsão de **Volatilidade Realizada** de ativos da B3. 

O projeto foi desenvolvido pela Diretoria de Data Science da Liga de Mercado Financeiro da UTFPR-AP como um MVP para demonstração técnica em eventos de investimentos, unindo modelos de Gradient Boosting de última geração com uma arquitetura de software robusta e escalável.

## 🎯 O Problema
No mercado de capitais, a volatilidade não é apenas uma medida de variação de preço, mas a principal métrica de **risco**. Prever a volatilidade futura é essencial para:
1. **Gestão de Risco:** Ajustar o tamanho das posições em portfólios.
2. **Derivativos:** Precificar opções através do modelo de Black-Scholes.
3. **Estratégia Quantitativa:** Identificar períodos de estresse ou calmaria no mercado.

## 🏗️ Arquitetura do Sistema
Seguimos uma **Layered Architecture (Arquitetura em Camadas)** para garantir a separação de responsabilidades, facilitando a manutenção e a integração futura com bancos de dados.

```text
volatility-api/
├── main.py              # Ponto de entrada e inicialização do servidor
├── app/
│   ├── api/             # Camada de Apresentação (Endpoints/Rotas)
│   ├── schemas/         # Camada de Validação (Contratos Pydantic)
│   └── services/        # Camada de Lógica de Negócio e Inferência ML
└── ml_models/           # Artefatos e modelos treinados (.joblib)

```
## 🛠️ Stack Tecnológica
- **Linguagem:** Python 3.14
- **Framework Web:** FastAPI (Alta performance e documentação automática)
- **Machine Learning:** LightGBM para modelagem e Optuna para otimização de hiperparâmetros.
- **Dados:** `yfinance` para extração de dados históricos diretamente da API do Yahoo Finance.
- **Validação:** Pydantic para tipagem estrita de dados de entrada e saída.

## 🚀 Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/PhilZeraNTC/volatility-api.git](https://github.com/PhilZeraNTC/volatility-api.git)
   cd volatility-api
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv venv
   ```
   Windows
   ```bash
   venv\Scripts\activate
   ```
   Linux/Mac
   ```bash
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install fastapi uvicorn yfinance lightgbm pydantic scikit-learn pandas
   ```

4. **Inicie o servidor:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Acesse a Documentação:**
   Acesse `http://127.0.0.1:8000/docs` para visualizar o Swagger UI e testar as previsões em tempo real.

## 🔌 API Documentation
### `GET /predict/{ticker}`
Retorna a volatilidade atual e a previsão para a janela futura.

**Parâmetros:**
- `ticker` (string): Código do ativo (ex: `PETR4.SA`)

**Exemplo de Resposta:**
```json
{
  "ticker": "PETR4.SA",
  "current_volatility": 0.2541,
  "predicted_volatility": 0.2815,
  "risk_status": "ALTO"
}
```

## 📈 Roadmap de Desenvolvimento
- [x] Setup da arquitetura base e FastAPI.
- [x] Mock de inferência para integração com Frontend.
- [ ] Treinamento final do modelo LightGBM para múltiplos ativos (PETR4, VALE3, IBOV).
- [ ] Implementação de Feature Engineering (RSI, Médias Móveis, Retornos Log).
- [ ] Integração com Dashboard interativo em React/TypeScript.

---
*Desenvolvido com foco em excelência técnica pela Diretoria de Data Science da Liga de Mercado Financeiro UTFPR-AP.*
