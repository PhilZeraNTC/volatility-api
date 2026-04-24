<script setup>
import MiniChart from './MiniChart.vue'

// Recebe o objeto do ativo como prop
defineProps(['ativo'])

// Define o evento de clique no botão deletar
const emit = defineEmits(['remover'])

// Função para formatar o nome do status
const formatStatus = (status) => {
  if (!status) return '---'
  return status.charAt(0).toUpperCase() + status.slice(1).toLowerCase()
}

// Função para calcular a data alvo (Hoje + 5 dias)
const getDataProjecao = () => {
  const d = new Date()
  d.setDate(d.getDate() + 5)
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })
}
</script>

<template>
  <div class="ativo-card fade-in">
    <div class="card-header">
      <div class="ticker-box">
        <span class="ticker-name">{{ ativo.ticker }}</span>
        <span :class="['risk-badge', ativo.risk_status]">
          {{ formatStatus(ativo.risk_status) }}
        </span>
      </div>
      <button @click="emit('remover', ativo.ticker)" class="btn-delete" title="Remover Ativo">&times;</button>
    </div>

    <div class="card-body">
      <div class="stat">
        <label>Volatilidade Atual</label>
        <div class="val">{{ (ativo.current_volatility * 100).toFixed(2) }}%</div>
      </div>
      <div class="divisor"></div>
      <div class="stat highlight">
        <label>Projeção para {{ getDataProjecao() }}</label>
        <div class="val">{{ (ativo.predicted_volatility * 100).toFixed(2) }}%</div>
      </div>
    </div>

    <div class="mini-chart-wrapper">
       <MiniChart :current="ativo.current_volatility" :predicted="ativo.predicted_volatility" />
    </div>
    
    <div class="card-footer">
      <span class="update-time">Análise Gerada via LGBM • {{ new Date().toLocaleDateString('pt-BR') }}</span>
    </div>
  </div>
</template>

<style scoped>
/* Mantive seus estilos que já estão ótimos */
.ativo-card {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 24px;
  width: 100%;
  max-width: 350px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.ativo-card:hover {
  transform: translateY(-5px);
  border-color: var(--accent);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ticker-name { 
  font-size: 1.4rem; 
  font-weight: 800; 
  color: var(--text-h); 
  letter-spacing: -0.5px;
}

.risk-badge {
  font-size: 0.65rem;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 6px;
  text-transform: uppercase;
  margin-left: 12px;
  vertical-align: middle;
}

.ALTO { 
  background: rgba(239, 68, 68, 0.15);
  color: #ff5f5f; 
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.NORMAL { 
  background: rgba(34, 197, 94, 0.15);
  color: #4ade80; 
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.BAIXO {
  background: rgba(14, 165, 233, 0.15);
  color: #7dd3fc;
  border: 1px solid rgba(14, 165, 233, 0.3);
}

.card-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.02);
  padding: 12px;
  border-radius: 12px;
}

.divisor {
  width: 1px;
  height: 30px;
  background: var(--border);
  opacity: 0.5;
}

.stat label { 
  font-size: 0.65rem; 
  text-transform: uppercase; 
  color: var(--text); 
  display: block;
  margin-bottom: 2px;
  font-weight: 600;
}

.stat .val { 
  font-size: 1.2rem; 
  font-weight: 700; 
  color: var(--text-h); 
}

.highlight .val { 
  color: var(--accent); 
}

.mini-chart-wrapper {
  width: 100%;
  height: 100px;
  opacity: 0.8;
}

.btn-delete { 
  background: rgba(255, 255, 255, 0.05); 
  border: none; 
  font-size: 1.2rem; 
  color: var(--text); 
  cursor: pointer; 
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s;
}

.btn-delete:hover { 
  background: rgba(239, 68, 68, 0.2);
  color: #ff5f5f; 
}

.card-footer {
  border-top: 1px solid var(--border);
  padding-top: 10px;
  text-align: center;
}

.update-time {
  font-size: 0.6rem;
  color: var(--text);
  opacity: 0.5;
  text-transform: uppercase;
  letter-spacing: 1px;
}
</style>
