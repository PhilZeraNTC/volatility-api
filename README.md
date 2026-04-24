# 📈 Volatility Predictor - Liga de Mercado Financeiro UTFPR

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.115-009688?style=for-the-badge&logo=fastapi)
![Vue.js](https://img.shields.io/badge/Vue.js-3.5-4FC08D?style=for-the-badge&logo=vuedotjs)
![Vite](https://img.shields.io/badge/Vite-6.0-646CFF?style=for-the-badge&logo=vite)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?style=for-the-badge&logo=chartdotjs)
![LightGBM](https://img.shields.io/badge/LightGBM-4.5.0-orange?style=for-the-badge)
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
.
├── main.py               # Ponto de entrada da API (FastAPI)
├── requirements.txt      # Dependências do ecossistema Python
├── ml_models/            # Modelos preditivos serializados (.joblib)
├── app/                  # Núcleo da aplicação
│   ├── api/              # Controladores e rotas
│   ├── schemas/          # Modelos de dados (Pydantic)
│   └── services/         # Engine de ML e engenharia de features
└── front/                # Interface do utilizador (Vite + Vue.js 3)
    ├── src/
    │   ├── components/   # Componentes modulares (Gráficos, Cards)
    │   └── pages/        # Views principais
    └── package.json      # Dependências do Frontend
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
   pip install -r requirements.txt
   ```

4. **Inicie o servidor:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Acesse a Documentação:**
   Acesse `http://127.0.0.1:8000/docs` para visualizar o Swagger UI e testar as previsões em tempo real.

## 🔌 API Documentation
### `GET /api/predict/{ticker}`
Retorna a volatilidade atual e a previsão para a janela futura.

**Parâmetros:**
- `ticker` (string): Código do ativo (ex: `PETR4.SA`)

**Exemplo de Resposta:**
```json
{
  "ticker": "PETR4.SA",
  "current_volatility": 0.2541,
  "predicted_volatility": 0.2815,
  "risk_status": "ALTO",
  "last_update": "23:48:10"
}
```
## Frontend (Dashboard Interativo)

A interface foi construída utilizando **Vue.js 3** com a **Composition API**, focando em uma experiência de usuário (UX) fluida e reativa para o monitoramento de riscos.

## 🛠️ Stack Tecnológica
* **Framework:** Vue.js 3 (Vite)
* **Gráficos:** Chart.js com integração `vue-chartjs`
* **Ícones:** Lucide Icons / SVG customizados
* **Estilização:** CSS3 Moderno (Variáveis e Animações customizadas)

## 🚀 Comandos de Inicialização

Certifique-se de ter o [Node.js](https://nodejs.org/) instalado (versão 18 ou superior).


1. **Navegar até o diretório do frontend**
```bash
cd front/src
```
2. **Instalar as dependências do projeto**
```bash
npm install
```
3. **Iniciar o servidor de desenvolvimento com Hot Reload**
```bash
npm run dev
```
4. **Gerar a versão de produção (Otimizada)**
```bash
npm run build
```
5. **Acesse a Dashboard:**
- Acesse o link do console para a versão de desenvolvimento.
- Acesse `http://127.0.0.1:8000/` para a versão de produção.

## 📈 Roadmap de Desenvolvimento
- [x] Setup da arquitetura base e FastAPI.
- [x] Mock de inferência para integração com Frontend.
- [x] Dashboard interativo com Vite + Vue.js 3.
- [ ] Cache de predições atualizado a 00:10 para otimização de requests.
- [ ] Treinamento final do modelo LightGBM para múltiplos ativos (PETR4, VALE3, IBOV).
- [x] Implementação de Feature Engineering (RSI, Médias Móveis, Retornos Log).


---
*Desenvolvido com foco em excelência técnica pela Diretoria de Data Science da Liga de Mercado Financeiro UTFPR-AP.*
