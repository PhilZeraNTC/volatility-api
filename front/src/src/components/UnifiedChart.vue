<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { 
  Chart as ChartJS, Title, Tooltip, Legend, LineElement, 
  LinearScale, PointElement, CategoryScale, Filler 
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale, Filler)

const props = defineProps(['ativos'])

// Paleta de cores para múltiplos ativos (Dourado, Azul, Verde, Rosa)
const cores = ['#f3bd48', '#3b82f6', '#10b981', '#ec4899']

const chartData = computed(() => {
  if (!props.ativos || props.ativos.length === 0) return { labels: [], datasets: [] }

  const formatarData = (diasAdicionais = 0) => {
    const d = new Date()
    d.setDate(d.getDate() + diasAdicionais)
    return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })
  }

const labels = [
    `Atual (${formatarData(0)})`, 
    `Previsto (${formatarData(5)})` // Simula os +5 dias da projeção
  ]  
  return {
    labels,
    datasets: props.ativos.map((ativo, index) => {
      const corSelecionada = cores[index % cores.length]
      
      const atual = ativo.current_volatility ? (ativo.current_volatility * 100).toFixed(2) : 0
      const previsto = ativo.predicted_volatility ? (ativo.predicted_volatility * 100).toFixed(2) : 0

      return {
        label: ativo.ticker || 'Ativo',
        data: [atual, previsto],
        borderColor: corSelecionada,
        // Gradiente suave abaixo da linha
        backgroundColor: (context) => {
          const ctx = context.chart.ctx
          const gradient = ctx.createLinearGradient(0, 0, 0, 400)
          gradient.addColorStop(0, corSelecionada + '33') // 20% opacidade
          gradient.addColorStop(1, corSelecionada + '00') // Transparente
          return gradient
        },
        borderWidth: 4,
        fill: true,
        tension: 0.4, // Curva suave
        pointRadius: 6,
        pointBackgroundColor: corSelecionada,
        pointBorderColor: '#13111a',
        pointBorderWidth: 2,
        pointHoverRadius: 8
      }
    })
  }
})

const options = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: {
      display: true,
      position: 'top',
      align: 'end',
      labels: { color: '#94a3b8', font: { family: 'Inter', size: 12, weight: '600' }, usePointStyle: true }
    },
    tooltip: {
      backgroundColor: '#1e1b26',
      titleColor: '#fff',
      bodyColor: '#94a3b8',
      padding: 12,
      cornerRadius: 10,
      borderColor: 'rgba(255,255,255,0.1)',
      borderWidth: 1,
      callbacks: {
        label: (context) => ` ${context.dataset.label}: ${context.raw}%`
      }
    }
  },
  scales: {
    y: {
      grid: { color: 'rgba(255,255,255,0.05)', drawBorder: false },
      ticks: { 
        color: '#64748b',
        callback: (value) => value + '%' 
      }
    },
    x: {
      grid: { display: false },
      ticks: { color: '#94a3b8', font: { weight: '600' } }
    }
  }
}
</script>

<template>
  <div class="unified-card fade-in">
    <div class="chart-header">
      <div class="header-main">
        <h3>Comparativo de Tendência</h3>
        <span class="badge">Live Analytics</span>
      </div>
      <p>Projeção de risco baseada em modelos de Machine Learning (LGBM)</p>
    </div>
    <div class="chart-container">
      <Line :data="chartData" :options="options" />
    </div>
  </div>
</template>

<style scoped>
.unified-card {
  background: #161a23; /* Mesma cor dos cards */
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  padding: 1.5rem;
  margin: 20px 0;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}
.chart-header {
  text-align: left;
  margin-bottom: 2rem;
}
.header-main {
  display: flex;
  align-items: center;
  gap: 12px;
}
.badge {
  background: var(--accent-bg);
  color: var(--accent);
  font-size: 0.7rem;
  padding: 4px 8px;
  border-radius: 6px;
  font-weight: bold;
  text-transform: uppercase;
}
.chart-header h3 { color: #f8fafc; margin: 0; font-size: 1.25rem; }
.chart-header p { color: #64748b; font-size: 0.85rem; margin-top: 4px; }
.chart-container { height: 380px; position: relative; }

/* Animação suave ao carregar */
.fade-in {
  animation: fadeIn 0.8s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
