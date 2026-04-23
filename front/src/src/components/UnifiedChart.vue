<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale)

const props = defineProps(['ativos'])

const gerarDatas = () => {
  const datas = []
  for (let i = 30; i >= 0; i--) {
    const d = new Date()
    d.setDate(d.getDate() - i)
    datas.push(d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' }))
  }
  datas.push("Projeção (7d)")
  return datas
}

const chartData = computed(() => {
  const labels = gerarDatas()
  
  return {
    labels,
    datasets: props.ativos.map((ativo, index) => {
      // Gera uma matiz (hue) baseada no index, saltando 137 graus 
      // (Proporção Áurea) para garantir que cores vizinhas sejam bem diferentes
      const hue = (index * 137.5) % 360;
      const color = `hsl(${hue}, 70%, 60%)`; // 70% saturação e 60% brilho para modo Dark
      
      const base = ativo.current_volatility
      const historicalData = Array.from({length: 31}, (_, i) => 
        base * (0.95 + (Math.random() * 0.1))
      )
      historicalData.push(ativo.predicted_volatility)

      return {
        label: ativo.ticker,
        data: historicalData,
        borderColor: color,
        backgroundColor: color.replace(')', ', 0.1)').replace('hsl', 'hsla'), // Fundo suave
        borderWidth: 2,
        tension: 0.3,
        pointRadius: 0,
        pointHitRadius: 10,
        pointHoverRadius: 6,
        pointHoverBackgroundColor: color,
        pointHoverBorderColor: '#fff',
        pointHoverBorderWidth: 2,
      }
    })
  }
})
const options = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false, // Faz a linha vertical e tooltip seguirem o mouse
  },
  plugins: {
  tooltip: {
    mode: 'index',
    intersect: false,
    backgroundColor: 'rgba(26, 22, 31, 0.9)',
    titleColor: '#fff',
    bodyFont: { size: 13 },
    usePointStyle: true, // Mostra uma bolinha da cor do ativo no tooltip
    callbacks: {
      label: (context) => ` ${context.dataset.label}: ${(context.raw * 100).toFixed(2)}%`
    }
  }
},
  scales: {
    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#666' } },
    x: { grid: { display: false }, ticks: { color: '#666', maxRotation: 0 } }
  }
}
</script>

<template>
  <div class="unified-card fade-in">
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
  width: 100%;
}
.chart-container { height: 500px; position: relative; }
</style>