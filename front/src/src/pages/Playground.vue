<script setup>
import { ref } from 'vue'
import AtivoCard from '../components/AtivoCard.vue'
import UnifiedChart from '../components/UnifiedChart.vue' // Importar novo componente

const listaAtivos = ref([])
const viewMode = ref('grid') // 'grid' ou 'unified'
const Ativo = ref('')
const carregando = ref(false)

async function buscar() {
  const t = Ativo.value.toUpperCase().trim()
  if (!t || listaAtivos.value.some(a => a.ticker === t)) return
  
  carregando.value = true
  try {
    const res = await fetch(`http://localhost:8000/predict/${t}`)
    const dados = await res.json()
    listaAtivos.value.unshift(dados)
    Ativo.value = ""
  } finally { carregando.value = false }
}

function remover(ticker) {
  listaAtivos.value = listaAtivos.value.filter(a => a.ticker !== ticker)
}
</script>

<template>
  <div class="page-container">
    
    <div class="toolbar fade-in">
      <div class="view-toggle">
        <button 
          @click="viewMode = 'grid'" 
          :class="{ active: viewMode === 'grid' }"
        >Cards</button>
        <button 
          @click="viewMode = 'unified'" 
          :class="{ active: viewMode === 'unified' }" 
          :disabled="listaAtivos.length === 0"
        >Comparativo</button>
      </div>

      <form @submit.prevent="buscar" class="search-form">
        <input v-model="Ativo" placeholder="Ticker (PETR4.SA)..." />
        <button type="submit" :disabled="carregando">+</button>
      </form>
    </div>

    <div class="content-area">
      <div v-if="viewMode === 'grid'" class="grid-layout fade-in">
        <AtivoCard 
          v-for="item in listaAtivos" 
          :key="item.ticker" 
          :ativo="item" 
          @remover="remover" 
        />
      </div>

      <div v-else class="unified-layout fade-in">
        <UnifiedChart :ativos="listaAtivos" />
      </div>

      <div v-if="listaAtivos.length === 0" class="empty">
        <p>Nenhum ativo monitorado. Adicione um ticker acima.</p>
      </div>
    </div>
    
  </div>
</template>

<style scoped>
.page-container {
  max-width: 1126px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.toolbar {
  display: inline-flex;
  align-items: center;
  gap: 15px;
  background: rgba(255, 255, 255, 0.03);
  padding: 10px 20px;
  border-radius: 20px;
  margin-bottom: 3rem;
  border: 1px solid var(--border);
}

.view-toggle {
  display: flex;
  background: var(--code-bg);
  padding: 4px;
  border-radius: 12px;
  border: 1px solid var(--border);
  height: 42px;
  box-sizing: border-box;
}

.view-toggle button {
  background: transparent;
  border: none;
  color: var(--text);
  padding: 0 15px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.2s;
  height: 100%;
}

.view-toggle button.active {
  background: var(--accent);
  color: white;
}

.search-form {
  display: flex;
  align-items: center;
  background: var(--code-bg);
  padding: 4px 4px 4px 15px;
  border-radius: 12px;
  border: 1px solid var(--border);
  height: 42px;
  width: 300px;
  box-sizing: border-box;
}

.search-form input {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--text-h);
  outline: none;
  font-size: 0.9rem;
}

.search-form button {
  background: var(--accent);
  color: white;
  border: none;
  width: 34px;
  height: 34px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}

.grid-layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 350px)); 
  gap: 24px;
  justify-content: center;
  width: 100%;
}

.empty { 
  text-align: center; 
  opacity: 0.5; 
  margin-top: 5rem; 
  color: var(--text);
}

.fade-in {
  animation: slideUp 0.5s ease-out forwards;
}
@media (max-width: 768px) {
  
  .toolbar { flex-direction: column; }
  
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>