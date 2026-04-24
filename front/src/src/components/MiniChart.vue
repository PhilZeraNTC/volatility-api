<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale, Filler } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale, Filler)

const props = defineProps(['current', 'predicted'])

// Mantemos a lógica das datas apenas para o Tooltip (quando passar o mouse)
const formatarData = (diasAdicionais) => {
  const d = new Date()
  d.setDate(d.getDate() + diasAdicionais)
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })
}

const chartData = computed(() => ({
  labels: [formatarData(-5), formatarData(0), formatarData(5)],
  datasets: [{
    borderColor: '#aa3bff',
    backgroundColor: 'rgba(170, 59, 255, 0.1)',
    data: [props.current * 0.95, props.current, props.predicted],
    fill: true,
    tension: 0.4,
    pointRadius: 0, // Remove os pontos para a linha ficar contínua e limpa
    pointHoverRadius: 5, // Só mostra o ponto quando passar o mouse
    pointBackgroundColor: '#aa3bff',
  }]
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { 
    legend: { display: false },
    tooltip: {
      enabled: true,
      backgroundColor: '#1e1b26',
      callbacks: {
        title: (items) => items[0].label, // Mostra a data no topo do balão
        label: (context) => ` Vol: ${context.raw.toFixed(2)}%`
      }
    }
  },
  scales: { 
    y: { display: false }, 
    x: { display: false } // AQUI: Removemos as datas e a linha do eixo X
  }
}
</script>

<template>
  <div class="chart-container">
    <Line :data="chartData" :options="options" />
  </div>
</template>

<style scoped>
.chart-container { 
  height: 90px; /* Ajuste leve para o card respirar */
  width: 100%; 
  margin-top: 5px; 
}
</style>
