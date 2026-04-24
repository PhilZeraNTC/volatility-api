import joblib
import pandas as pd
import numpy as np
import yfinance as yf
import threading
from datetime import datetime, timedelta
from pathlib import Path

# Configuração de caminhos: subindo 3 níveis para chegar na raiz onde está ml_models/
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "ml_models" / "lightgbm_model.joblib"

class PredictVolatilityService:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Modelo não encontrado em: {MODEL_PATH}")
        
        self.model = joblib.load(MODEL_PATH)
        self._cache = {}
        self._cache_duration = timedelta(hours=12)
        self.window = 21
        self.features_list = [
            'target_vol', 'lag_vol_1', 'lag_vol_5', 'returns_sq', 'ema_returns',
            'parkinson_vol', 'vol_media_5d', 'vol_media_21d',
            'vol_media_63d', 'skew_21', 'kurt_21',
            'retorno_ibov', 'retorno_dolar', 'rsi_14', 'bb_distancia_topo'
        ]

    def fetch_market_data(self, ticker: str):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=150)

        df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True, progress=False)
        if df.empty or len(df) < 64:
            raise ValueError(f"{ticker}: Ativo não encontrado.")
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        macro = yf.download(['^BVSP', 'BRL=X'], start=start_date, end=end_date, progress=False)['Close']
        
        # Sincroniza e preenche buracos
        df = df.ffill()
        macro = macro.ffill()
        
        return df, macro

    def prepare_features(self, df: pd.DataFrame, macro: pd.DataFrame):
        # Cálculos de Volatilidade e Retornos
        df['returns'] = np.log(df['Close'] / df['Close'].shift(1))
        df['target_vol'] = df['returns'].rolling(window=self.window).std() * np.sqrt(252)
        df['lag_vol_1'] = df['target_vol'].shift(1)
        df['lag_vol_5'] = df['target_vol'].shift(5)
        df['returns_sq'] = df['returns']**2
        df['ema_returns'] = df['returns'].ewm(span=self.window).mean()

        # Parkinson
        rs = (1.0 / (4.0 * np.log(2.0))) * (np.log(df['High'] / df['Low']) ** 2)
        df['parkinson_vol'] = np.sqrt(rs.rolling(window=self.window).mean()) * np.sqrt(252)

        # Médias Móveis
        df['vol_media_5d'] = df['target_vol'].rolling(window=5).mean()
        df['vol_media_21d'] = df['target_vol'].rolling(window=21).mean()
        df['vol_media_63d'] = df['target_vol'].rolling(window=63).mean()

        # Estatísticas
        df['skew_21'] = df['returns'].rolling(window=self.window).skew()
        df['kurt_21'] = df['returns'].rolling(window=self.window).kurt()

        # Macro
        df['retorno_ibov'] = np.log(macro['^BVSP'] / macro['^BVSP'].shift(1)).fillna(0)
        df['retorno_dolar'] = np.log(macro['BRL=X'] / macro['BRL=X'].shift(1)).fillna(0)

        # Técnicos
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        df['rsi_14'] = 100 - (100 / (1 + (gain / loss)))

        bb_media = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['bb_distancia_topo'] = (bb_media + (2 * bb_std)) - df['Close']

        # --- RESILIÊNCIA CONTRA NaNs ---
        # Filtramos apenas as colunas que o modelo usa e removemos linhas incompletas (ex: hoje)
        df_limpo = df[self.features_list].dropna()

        if df_limpo.empty:
            # Tenta preencher vazios se o dropna limpou tudo (comum em fechamento de mercado)
            df_limpo = df[self.features_list].ffill().dropna()
            
        if df_limpo.empty:
            raise ValueError("Erro: Dados históricos insuficientes para calcular as 15 features.")

        # Pegamos a última linha válida
        X_input = df_limpo.tail(1)
        vol_referencia = df.loc[X_input.index[0], 'target_vol']

        # Validação de sanidade na volatilidade atual
        if np.isnan(vol_referencia):
            raise ValueError("Volatilidade atual corrompida (NaN).")
        
        if vol_referencia > 1.0:
            raise ValueError(
                f"Volatilidade atual fora do range esperado ({vol_referencia:.2%}). "
                f"Possível dado corrompido ou ativo ilíquido com gap extremo."
            )

        return X_input, vol_referencia

    def get_prediction_data(self, ticker: str):
        if not ticker.endswith('.SA') and '^' not in ticker and '=' not in ticker:
            ticker = f"{ticker.upper()}.SA"

        agora = datetime.now()
        cached_item = self._cache.get(ticker)

        if not cached_item:
            return self._execute_update(ticker)

        if agora > cached_item['expiry'] and not cached_item['is_updating']:
            thread = threading.Thread(target=self._execute_update, args=(ticker,))
            thread.start()

        return cached_item['data']

    def _execute_update(self, ticker: str):
        if ticker in self._cache:
            self._cache[ticker]['is_updating'] = True

        try:
            df, macro = self.fetch_market_data(ticker)
            X_input, vol_atual = self.prepare_features(df, macro)
            
            # Validação crucial: Se vol_atual for NaN, interrompa!
            if np.isnan(vol_atual):
                raise ValueError("Dados de volatilidade corrompidos no provedor.")

            delta_previsto = self.model.predict(X_input)[0]
            
            # Se o modelo falhar e retornar NaN
            if np.isnan(delta_previsto):
                delta_previsto = 0 

            previsao_final = float(np.clip(vol_atual + delta_previsto, 0.01, 0.60))

            # Nova lógica de thresholds:
            if previsao_final >= 0.40:
                status = "ALTO"
            elif previsao_final >= 0.20:
                status = "MODERADO"
            else:
                status = "NORMAL"

            resultado = {
                "ticker": ticker,
                "current_volatility": float(vol_atual),
                "predicted_volatility": previsao_final,
                "risk_status": status,
                "last_update": datetime.now().strftime("%H:%M:%S")
            }

            self._cache[ticker] = {
                'data': resultado,
                'expiry': datetime.now() + self._cache_duration,
                'is_updating': False
            }
            return resultado

        except Exception as e:
            if ticker in self._cache:
                self._cache[ticker]['is_updating'] = False
            raise e

predictor = PredictVolatilityService()
