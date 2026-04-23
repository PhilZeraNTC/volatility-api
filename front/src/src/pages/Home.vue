<script setup>
import { ref } from 'vue'
import LigaLogo from '../assets/Liga.svg'


// Variável reativa para controlar se o menu de celular está aberto ou fechado
const menuAberto = ref(false)
//Variáveis ligadas aos inputs do formulário
const Ativo = ref('')
//Variaveis de reposta
const resultadoAPI = ref(null)
// Controle de estado
const carregando = ref(false)
const erro = ref('')
// Função para alternar o estado do menu
function alternarMenu() {
  menuAberto.value = !menuAberto.value
}

async function buscarDados() {
  // Evita buscar se o input estiver vazio
  if (!Ativo.value) return

  carregando.value = true
  erro.value = ''
  resultadoAPI.value = null // Limpa o resultado anterior

  try {
    // Passamos o texto digitado como um parâmetro de query na URL (?q=...)
    const url = `http://localhost:8000/predict/${encodeURIComponent(Ativo.value)}`
    
    const resposta = await fetch(url) // O fetch já é GET por padrão!

    if (!resposta.ok) {
      throw new Error(`Erro: ${resposta.status}`)
    }

    // Pega a resposta e transforma no objeto JSON
    const dadosJson = await resposta.json()
    
    // Salva o JSON na variável reativa para aparecer na tela
    resultadoAPI.value = dadosJson

  } catch (e) {
    erro.value = 'Ativo não encontrado.'
    console.error(e)
  } finally {
    carregando.value = false
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
            <input 
              type="text" 
              v-model="Ativo" 
              placeholder="Ex: PETR4.SA"
              required
            />
          </div>
          <button type="submit" :disabled="carregando" class="btn-primary">
            <span v-if="!carregando">Analisar Ativo</span>
            <span v-else class="loader"></span>
          </button>
        </form>

        <p v-if="erro" class="erro-msg">{{ erro }}</p>
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
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="accent-icon"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
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
/* Reaproveitando suas variáveis do root */

.container {
  max-width: 1126px;
  margin: 0 auto;
  padding: 0.8rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Logo UX */

/* Seção de Busca */
.search-section {
  text-align: center;
  margin-bottom: 2rem;
}

.kicker {
  color: var(--accent);
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.description {
  max-width: 400px;
  margin: 0 auto 2rem;
  font-size: 0.95rem;
}

.formulario-busca {
  display: flex;
  background: var(--bg);
  padding: 8px;
  border: 1px solid var(--border);
  border-radius: 12px;
  box-shadow: var(--shadow);
  max-width: 450px;
  margin: 0 auto;
  transition: border-color 0.3s;
}

.formulario-busca:focus-within {
  border-color: var(--accent);
}

input {
  flex: 1;
  border: none;
  padding: 10px 15px;
  background: transparent;
  color: var(--text-h);
  font-family: var(--sans);
  font-size: 1rem;
}

input:focus { outline: none; }

.btn-primary {
  background: var(--accent);
  color: #fff;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-primary:hover { opacity: 0.9; }

/* Card de Resultado (Onde o UX brilha) */
.card-resultado {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 16px;
  width: 100%;
  max-width: 500px;
  overflow: hidden;
  box-shadow: var(--shadow);
  margin-top: 2rem;
}

.card-header {
  padding: 1.5rem;
  background: var(--social-bg);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border);
}

.ticker-badge {
  font-family: var(--mono);
  font-weight: 700;
  font-size: 1.2rem;
  color: var(--text-h);
}

.risk-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
}

.risk-badge.ALTO { background: #fee2e2; color: #991b1b; }
.risk-badge.NORMAL { background: #dcfce7; color: #166534; }
.risk-badge.BAIXO { background: #e0f2fe; color: #075985; }

.card-body {
  padding: 2rem;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.data-point label {
  display: block;
  font-size: 0.8rem;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.data-point .value {
  font-size: 1.8rem;
  font-weight: 500;
  color: var(--text-h);
}

.data-point.highlight .value {
  color: var(--accent);
  font-weight: 700;
}

.divider-v {
  width: 1px;
  height: 50px;
  background: var(--border);
}

/* Mobile */
@media (max-width: 768px) {
  
  .card-body { flex-direction: column; gap: 20px; }
  .divider-v { display: none; }
}

.fade-in {
  animation: fadeIn 0.5s ease forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.sobre-section {
  padding: 80px 20px;
  background: var(--bg);
  border-top: 1px solid var(--border);
}

.sobre-container {
  max-width: 1126px;
  margin: 0 auto;
}

.sobre-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 60px;
  align-items: center;
}

.sobre-content {
  text-align: left;
}

.sobre-content h2 {
  font-size: 2.5rem;
  margin: 10px 0 20px;
  color: var(--text-h);
}

.sobre-content p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--text);
  margin-bottom: 20px;
}

.sobre-card {
  background: var(--code-bg);
  padding: 40px;
  border-radius: 20px;
  border: 1px solid var(--border);
  text-align: left;
  box-shadow: var(--shadow);
}

.icon-box {
  background: var(--accent-bg);
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.accent-icon {
  color: var(--accent);
}

.sobre-card h3 {
  color: var(--text-h);
  margin-bottom: 15px;
}

.sobre-card p {
  font-size: 0.95rem;
  color: var(--text);
  line-height: 1.5;
}

/* Ajuste Responsivo */
@media (max-width: 900px) {
  .sobre-grid {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  
  .sobre-content h2 {
    font-size: 2rem;
  }
}
</style>