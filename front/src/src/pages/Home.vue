<script setup>
import { ref } from 'vue'
import LigaLogo from '../assets/Liga.svg'


// Variável reativa para controlar se o menu de celular está aberto ou fechado
const menuAberto = ref(false)
//Variáveis ligadas aos inputs do formulário
const Ativo = ref('')
//Variaveis de reposta
const resultadoAPI = ref(null)
const showSpinner = ref(false)
// Controle de estado
const carregando = ref(false)
const erro = ref('')
// Função para alternar o estado do menu
function alternarMenu() {
  menuAberto.value = !menuAberto.value
}

async function buscarDados() {
  if (!Ativo.value) return;

  carregando.value = true;
  showSpinner.value = false;
  erro.value = '';
  resultadoAPI.value = null;

  const timer = setTimeout(() => {
    if (carregando.value) showSpinner.value = true;
  }, 0.1);

  try {
    const url = `http://localhost:8000/api/predict/${encodeURIComponent(Ativo.value)}`;
    const resposta = await fetch(url);

    // 1. Primeiro, pegamos a resposta como TEXTO
    const textoPuro = await resposta.text();

    // 2. Agora tentamos transformar em JSON manualmente
    let dados;
    try {
      dados = JSON.parse(textoPuro);
    } catch (e) {
      // Se cair aqui, a API retornou um erro HTML ou texto (ex: Erro 500 do Servidor)
      console.error("Conteúdo recebido não é JSON:", textoPuro);
      throw new Error("ERRO: NÃO ENCONTRADO OU INEXISTENTE");
    }

    if (!resposta.ok) {
      throw new Error(dados.detail || `Erro técnico: ${resposta.status}`);
    }

    resultadoAPI.value = dados;

  } catch (e) {
    erro.value = e.message;
  } finally {
    clearTimeout(timer);
    carregando.value = false;
    showSpinner.value = false;
  }
}
</script>

<template>
  <main id="app">
    <section id="center">
      <div class="search-section">
        <span class="kicker">Análise de Risco</span>
        <h1>Previsão de Ativos</h1>
        <p class="description">Insira o ticker do ativo para calcular a volatilidade prevista via ML.</p>

        <form @submit.prevent="buscarDados" class="formulario-busca">
          <div class="input-wrapper">
            <input type="text" v-model="Ativo" placeholder="Ex: PETR4.SA" required />
          </div>
          <button type="submit" :disabled="carregando" class="btn-primary">
            <span :class="{ 'text-hidden': showSpinner }">Analisar Ativo</span>

            <div v-if="showSpinner" class="loader-container">
              <div class="loader"></div>
            </div>
          </button>
        </form>

        <p v-if="erro" class="erro-msg fade-in">{{ erro }}</p>
      </div>

      <div v-if="resultadoAPI" class="card-resultado fade-in">
        <div class="card-header">
          <span class="ticker-badge">{{ resultadoAPI.ticker }}</span>
          <span :class="['risk-badge', resultadoAPI.risk_status]">
            Risco {{ resultadoAPI.risk_status }}
          </span>
        </div>

        <div class="card-body">
          <div class="data-point">
            <label>Volatilidade Atual</label>
            <div class="value">{{ (resultadoAPI.current_volatility * 100).toFixed(2) }}%</div>
          </div>
          <div class="divider-v"></div>
          <div class="data-point highlight">
            <label>Previsão (Próximos Dias)</label>
            <div class="value">{{ (resultadoAPI.predicted_volatility * 100).toFixed(2) }}%</div>
          </div>
        </div>
      </div>
    </section>

    <div id="spacer"></div>
  </main>
  <section id="sobre" class="sobre-section">
    <div class="sobre-container">
      <div class="sobre-grid">
        <div class="sobre-content">
          <span class="kicker">Quem Somos</span>
          <h2>Liga de Mercado Financeiro</h2>
          <p>
            A <strong>Liga de Mercado Financeiro da UTFPR</strong> é uma organização estudantil
            formada exclusivamente por alunos das Engenharias. Nosso objetivo é preencher a lacuna entre
            o ambiente acadêmico técnico e o dinamismo do setor financeiro.
          </p>
          <p>
            Unimos o rigor analítico da engenharia com a paixão pelas finanças, promovendo
            estudos sobre análise de ativos, gestão de risco e modelagem quantitativa.
          </p>
        </div>

        <div class="sobre-card">
          <div class="icon-box">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="accent-icon">
              <path
                d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z">
              </path>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
          </div>
          <h3>O Aplicativo</h3>
          <p>
            O <strong>Volatility Predictor</strong> é uma ferramenta de suporte à decisão que utiliza
            algoritmos de aprendizado de máquina para estimar a volatilidade futura de ativos da B3.
            Ele ajuda investidores a compreenderem o risco potencial de um ativo antes de realizar operações.
          </p>
        </div>
      </div>
    </div>
  </section>


</template>

<style scoped>
/* 1. Layout Base */
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}

#center {
  width: 100%;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 2. Seção de Busca */
.search-section {
  text-align: center;
  margin-bottom: 2rem;
  width: 100%;
}

.kicker {
  color: var(--accent);
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  display: block;
  margin-bottom: 0.5rem;
}

.description {
  max-width: 450px;
  margin: 0 auto 2rem;
  font-size: 0.95rem;
  color: var(--text);
}

/* 3. Formulário de Busca com Spinner na Borda */
.formulario-busca {
  display: flex;
  align-items: center;
  background: var(--code-bg);
  padding: 6px;
  border: 1px solid var(--border);
  border-radius: 14px;
  box-shadow: var(--shadow);
  max-width: 450px;
  width: 100%;
  margin: 0 auto;
  transition: all 0.3s ease;
}

.formulario-busca:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px rgba(170, 59, 255, 0.2);
}

.input-wrapper {
  flex: 1;
}

input {
  width: 100%;
  border: none;
  padding: 10px 15px;
  background: transparent;
  color: var(--text-h);
  font-size: 1rem;
  outline: none;
}

/* Botão de Ação */
.btn-primary {
  position: relative;
  /* Essencial para posicionar o loader por cima */
  background: var(--accent);
  color: #ffffff;
  font-weight: bolder;
  border: none;
  padding: 10px 24px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 150px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.text-hidden {
  opacity: 0;
}
.loader-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.btn-primary:hover:not(:disabled) {
  filter: brightness(1.1);
  transform: translateY(-1px);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Animação de Carregamento (Spinner) */
.loader {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
/* 4. Card de Resultado Profissional */
.card-resultado {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 20px;
  width: 100%;
  max-width: 550px;
  overflow: hidden;
  box-shadow: var(--shadow);
  margin-top: 3rem;
}

.card-header {
  padding: 1.2rem 2rem;
  background: rgba(255, 255, 255, 0.02);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border);
}

.ticker-badge {
  font-family: var(--mono);
  font-weight: 800;
  font-size: 1.3rem;
  color: var(--text-h);
  letter-spacing: -0.5px;
}

/* Badges Neon de Risco */
.risk-badge {
  padding: 6px 14px;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
}

.risk-badge.ALTO {
  background: rgba(239, 68, 68, 0.15);
  color: #ff5f5f;
  border: 1px solid rgba(239, 68, 68, 0.5);
}

.risk-badge.NORMAL {
  background: rgba(34, 197, 94, 0.15);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.5);
}

.risk-badge.BAIXO {
  background: rgba(14, 165, 233, 0.15);
  color: #7dd3fc;
  border: 1px solid rgba(14, 165, 233, 0.5);
}

.card-body {
  padding: 2.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.data-point label {
  display: block;
  font-size: 0.7rem;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text);
}

.data-point .value {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-h);
}

.data-point.highlight .value {
  color: var(--accent);
}

.divider-v {
  width: 1px;
  height: 60px;
  background: var(--border);
  opacity: 0.5;
}

/* 5. Seção Sobre */
.sobre-section {
  padding: 100px 20px;
  background: var(--bg);
  border-top: 1px solid var(--border);
  width: 100%;
}

.sobre-container {
  max-width: 1126px;
  margin: 0 auto;
}

.sobre-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 60px;
  align-items: start;
}

.sobre-content h2 {
  font-size: 2.5rem;
  margin: 10px 0 20px;
  color: var(--text-h);
}

.sobre-card {
  background: var(--code-bg);
  padding: 40px;
  border-radius: 24px;
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
}

.icon-box {
  background: rgba(170, 59, 255, 0.1);
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  color: var(--accent);
}

/* Animações e Responsividade */
.fade-in {
  animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .sobre-grid {
    grid-template-columns: 1fr;
  }

  .card-body {
    flex-direction: column;
    gap: 30px;
    text-align: center;
  }

  .divider-v {
    display: none;
  }

.formulario-busca {
    flex-direction: column;
    gap: 10px;
    background: transparent;
    border: none;
    box-shadow: none;
  }
  .input-wrapper, .btn-primary {
    width: 100%;
    background: var(--code-bg);
    border: 1px solid var(--border);
  }
  .btn-primary {
    background: var(--accent);
  }
}
.erro-msg {
  color: #ff5f5f;
  background: rgba(239, 68, 68, 0.1);
  padding: 10px;
  border-radius: 8px;
  margin-top: 1rem;
  font-size: 0.9rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
}
</style>