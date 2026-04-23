<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale, Filler } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale, Filler)

const props = defineProps(['current', 'predicted'])

const chartData = computed(() => ({
  labels: ['Hist.', 'Hoje', 'Proj.'],
  datasets: [{
    borderColor: '#aa3bff',
    backgroundColor: 'rgba(170, 59, 255, 0.1)',
    data: [props.current * 0.95, props.current, props.predicted],
    fill: true,
    tension: 0.4,
    pointRadius: 3
  }]
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: { y: { display: false }, x: { grid: { display: false } } }
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