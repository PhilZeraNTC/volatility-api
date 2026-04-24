<script setup>
import { ref } from 'vue'
import AtivoCard from '../components/AtivoCard.vue'
import UnifiedChart from '../components/UnifiedChart.vue'

const listaAtivos = ref([])
const viewMode = ref('grid')
const Ativo = ref('')
const carregando = ref(false)
const erro = ref('')

async function buscar() {
  const t = Ativo.value.toUpperCase().trim()
  if (!t) return
  if (listaAtivos.value.some(a => a.ticker === t)) {
    erro.value = "Este ativo já foi adicionado."
    return
  }

  carregando.value = true
  erro.value = ''

  try {
    const res = await fetch(`http://localhost:8000/api/predict/${t}`)
    const dados = await res.json()

    if (!res.ok) {
      erro.value = dados.detail || "Ativo não encontrado ou dados insuficientes."
      return
    }

    listaAtivos.value.unshift(dados)
    Ativo.value = ""
    // Se for o primeiro ativo, garante que está no modo grid
    if(listaAtivos.value.length === 1) viewMode.value = 'grid'
    
  } catch (e) {
    erro.value = "Erro de conexão com o servidor."
  } finally {
    carregando.value = false
  }
}

function remover(ticker) {
  listaAtivos.value = listaAtivos.value.filter(a => a.ticker !== ticker)
  if (listaAtivos.value.length === 0) viewMode.value = 'grid'
}
</script>

<template>
  <div class="page-container">
    <div class="header-section fade-in">
      <h1>Playground de Volatilidade</h1>
      <p>Monitore múltiplos ativos e compare projeções de risco em tempo real.</p>
    </div>

    <div class="toolbar fade-in">
      <div class="view-toggle">
        <button @click="viewMode = 'grid'" :class="{ active: viewMode === 'grid' }">
          <span class="icon">🗂️</span> Cards
        </button>
        <button @click="viewMode = 'unified'" :class="{ active: viewMode === 'unified' }"
          :disabled="listaAtivos.length === 0">
          <span class="icon">📊</span> Comparativo
        </button>
      </div>

      <form @submit.prevent="buscar" class="search-form" :class="{ 'is-loading': carregando }">
        <input v-model="Ativo" placeholder="Ex: PETR4.SA" :disabled="carregando" />
        <button type="submit" :disabled="carregando">
          <span v-if="!carregando">+</span>
          <span v-else class="spinner"></span>
        </button>
      </form>
    </div>

    <Transition name="slide-fade">
      <div v-if="erro" class="error-banner">
        <span class="error-icon">⚠️</span> {{ erro }}
        <button @click="erro = ''" class="close-error">×</button>
      </div>
    </Transition>

    <div class="content-area">
      <div v-if="viewMode === 'grid'" class="grid-layout fade-in">
        <AtivoCard v-for="item in listaAtivos" :key="item.ticker" :ativo="item" @remover="remover" />
      </div>

      <div v-else-if="viewMode === 'unified' && listaAtivos.length > 0" class="unified-layout fade-in">
        <UnifiedChart :ativos="listaAtivos" />
      </div>

      <div v-if="listaAtivos.length === 0 && !carregando" class="empty fade-in">
        <div class="empty-icon">📈</div>
        <p>Sua lista está vazia.</p>
        <span>Digite um ticker acima para começar a análise.</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Adicionando ao que você já tem */
.header-section { margin-bottom: 2rem; }
.header-section h1 { font-size: 2rem; margin-bottom: 0.5rem; }
.header-section p { color: var(--text); font-size: 1rem; }

.toolbar {
  display: inline-flex;
  backdrop-filter: blur(10px);
  background: rgba(22, 26, 35, 0.6);
  z-index: 10;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: block;
}

@keyframes spin { to { transform: rotate(360deg); } }

.slide-fade-enter-active, .slide-fade-leave-active { transition: all 0.3s ease; }
.slide-fade-enter-from, .slide-fade-leave-to { opacity: 0; transform: translateY(-10px); }

.error-banner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  position: relative;
}

.close-error {
  background: transparent;
  border: none;
  color: #ff5f5f;
  font-size: 1.2rem;
  cursor: pointer;
  margin-left: 10px;
}

.empty-icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.3; }
.empty span { font-size: 0.85rem; opacity: 0.6; }

@media (max-width: 768px) {
  .toolbar { flex-direction: column; width: 100%; }
  .search-form { width: 100%; }
}
</style>
