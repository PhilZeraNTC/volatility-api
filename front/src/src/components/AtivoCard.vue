<script setup>
import MiniChart from './MiniChart.vue'

// Recebe o objeto do ativo como prop
defineProps(['ativo'])

// Define o evento de clique no botão deletar
const emit = defineEmits(['remover'])
</script>

<template>
  <div class="ativo-card fade-in">
    <div class="card-header">
      <div class="ticker-box">
        <span class="ticker-name">{{ ativo.ticker }}</span>
        <span :class="['risk-badge', ativo.risk_status]">{{ ativo.risk_status }}</span>
      </div>
      <button @click="emit('remover', ativo.ticker)" class="btn-delete">&times;</button>
    </div>

    <div class="card-body">
      <div class="stat">
        <label>Atual</label>
        <div class="val">{{ (ativo.current_volatility * 100).toFixed(2) }}%</div>
      </div>
      <div class="stat highlight">
        <label>Projeção</label>
        <div class="val">{{ (ativo.predicted_volatility * 100).toFixed(2) }}%</div>
      </div>
    </div>

    <div class="mini-chart-wrapper">
       <MiniChart :current="ativo.current_volatility" :predicted="ativo.predicted_volatility" />
    </div>
  </div>
</template>

<style scoped>
.ativo-card {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 20px;
  width: 320px; /* LARGURA FIXA PARA NÃO ESPALHAR */
  display: flex;
  flex-direction: column; /* FORÇA UM ABAIXO DO OUTRO */
  gap: 15px;
  box-shadow: var(--shadow);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-body {
  display: flex;
  justify-content: space-between; /* Coloca Atual na esquerda e Projeção na direita */
  text-align: left;
}

.mini-chart-wrapper {
  width: 100%;
  height: 120px; /* Garante espaço para o gráfico */
}

/* Animação ao passar o mouse */
.ativo-card:hover {
  transform: scale(1.03);
  border-color: var(--accent-border);
}


.risk-badge {
  font-size: 0.7rem;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 8px;
  text-transform: uppercase;
  margin-left: 10px;
  display: inline-block;
  line-height: 1;
}

/* CORES PARA DARK MODE (Contraste Máximo) */

/* Risco Alto: Fundo Vermelho Escuro com Texto Vermelho Vivo ou Branco */
.ALTO { 
  background: rgba(239, 68, 68, 0.2); /* Vermelho translúcido */
  color: #ff5f5f;                     /* Vermelho bem claro/vivo */
  border: 1px solid #ef4444; 
}

/* Risco Normal: Fundo Verde Escuro com Texto Verde Vivo */
.NORMAL { 
  background: rgba(34, 197, 94, 0.2);  /* Verde translúcido */
  color: #4ade80;                      /* Verde bem claro/vivo */
  border: 1px solid #22c55e; 
}

/* Caso tenhas Risco Baixo: Azul */
.BAIXO {
  background: rgba(14, 165, 233, 0.2);
  color: #7dd3fc;
  border: 1px solid #0ea5e9;
}


.ticker-name { font-size: 1.2rem; font-weight: 800; color: var(--text-h); }
.risk-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-left: 5px; }


.btn-delete { background: none; border: none; font-size: 1.5rem; color: var(--text); cursor: pointer; }
.btn-delete:hover { color: #ef4444; }


.stat label { font-size: 0.6rem; text-transform: uppercase; color: var(--text); display: block; }
.stat .val { font-size: 1.3rem; font-weight: 700; color: var(--text-h); }
.highlight .val { color: var(--accent); }
</style>