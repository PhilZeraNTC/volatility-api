<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale, Filler } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale, Filler)

const props = defineProps(['current', 'predicted'])

// Função para formatar as datas no eixo X
const formatarData = (diasAdicionais) => {
  const d = new Date()
  d.setDate(d.getDate() + diasAdicionais)
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })
}

const chartData = computed(() => ({
  // Agora usamos as datas reais: 5 dias atrás, Hoje e daqui a 5 dias
  labels: [formatarData(-5), formatarData(0), formatarData(5)],
  datasets: [{
    borderColor: '#aa3bff',
    backgroundColor: 'rgba(170, 59, 255, 0.1)',
    data: [props.current * 0.95, props.current, props.predicted],
    fill: true,
    tension: 0.4,
    pointRadius: 4, // Aumentei um pouco para facilitar a visão no card
    pointBackgroundColor: '#aa3bff',
  }]
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { 
    legend: { display: false },
    tooltip: {
      enabled: true, // Ativei o tooltip para o usuário ver a data ao passar o mouse
      backgroundColor: '#1e1b26',
      callbacks: {
        label: (context) => ` Vol: ${context.raw.toFixed(2)}%`
      }
    }
  },
  scales: { 
    y: { display: false }, 
    x: { 
      grid: { display: false },
      ticks: {
        color: '#64748b',
        font: { size: 10, weight: '600' }
      }
    } 
  }
}
</script>

<template>
  <div class="chart-container">
    <Line :data="chartData" :options="options" />
  </div>
</template>

<style scoped>
.chart-container { height: 100px; width: 100%; margin-top: 10px; }
</style>
