<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { 
  Chart as ChartJS, Title, Tooltip, Legend, LineElement, 
  LinearScale, PointElement, CategoryScale, Filler 
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale, Filler)

const props = defineProps(['ativos'])

const chartData = computed(() => {
  // Se a lista estiver vazia, retorna um objeto básico para evitar erro de undefined
  if (!props.ativos || props.ativos.length === 0) {
    return { labels: [], datasets: [] }
  }

  const labels = ['Volatilidade Atual', 'Projeção (LGBM +5d)']
  
  return {
    labels,
    datasets: props.ativos.map((ativo, index) => {
      const hue = (index * 137.5) % 360;
      const color = `hsl(${hue}, 75%, 60%)`;
      
      // Garantimos que os valores são números válidos antes de passar para o Chart.js
      const atual = ativo.current_volatility ? (ativo.current_volatility * 100).toFixed(2) : 0;
      const previsto = ativo.predicted_volatility ? (ativo.predicted_volatility * 100).toFixed(2) : 0;

      return {
        label: ativo.ticker || 'Desconhecido',
        data: [atual, previsto],
        borderColor: color,
        backgroundColor: color.replace('hsl', 'hsla').replace(')', ', 0.1)'),
        borderWidth: 4,
        fill: true,
        tension: 0.4,
        pointRadius: 6,
        pointBackgroundColor: color,
        pointHoverRadius: 8
      }
    })
  }
})
const options = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  plugins: {
    legend: {
      display: true,
      position: 'bottom',
      labels: { color: '#888', font: { weight: '600' }, padding: 20 }
    },
    tooltip: {
      backgroundColor: '#1a161f',
      titleColor: '#fff',
      padding: 15,
      borderColor: 'rgba(255,255,255,0.1)',
      borderWidth: 1,
      callbacks: {
        label: (context) => ` ${context.dataset.label}: ${context.raw}% a.a.`
      }
    }
  },
  scales: {
    y: {
      grace: '5%',
      grid: { color: 'rgba(255,255,255,0.05)' },
      ticks: { 
        color: '#666',
        callback: (value) => value + '%' // Formata como porcentagem
      },
      title: { display: true, text: 'Volatilidade Anualizada', color: '#444' }
    },
    x: {
      grid: { display: false },
      ticks: { color: '#888', font: { weight: 'bold' } }
    }
  }
}
</script>

<template>
  <div class="unified-card fade-in">
    <div class="chart-header">
      <h3>Comparativo de Tendência</h3>
      <p>Análise de variação prevista para os próximos 5 pregões</p>
    </div>
    <div class="chart-container">
      <Line :data="chartData" :options="options" />
    </div>
  </div>
</template>

<style scoped>
.unified-card {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 2rem;
  margin-top: 10px;
}
.chart-header {
  text-align: left;
  margin-bottom: 1.5rem;
}
.chart-header h3 { color: var(--text-h); margin-bottom: 5px; }
.chart-header p { color: #666; font-size: 0.9rem; }
.chart-container { height: 450px; }
</style>
