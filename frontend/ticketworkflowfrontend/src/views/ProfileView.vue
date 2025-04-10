<template>
    <div class="profile-view">
      <h2>Twój profil</h2>
      
      <div class="stats-grid">
        <div class="stat-card gradient-purple">
          <h3 class="header">Aktywność</h3>
          <div class="stat-value">{{ activity }}</div>
          <div class="stat-label">Punkty aktywności</div>
        </div>
        
        <div class="stat-card gradient-blue">
          <h3 class="header">Ostatnie zgłoszenie</h3>
          <div class="stat-value">{{ lastTicketDate }}</div>
          <div class="stat-label">Data ostatniej aktywności</div>
        </div>
      </div>
  
      <div class="progress-chart">
        <h3>Postęp zgłoszeń</h3>
        <canvas ref="chart"></canvas>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import Chart from 'chart.js/auto'
  import { useTicketStore } from '../stores/ticketStore'
  
  const ticketStore = useTicketStore()
  const chart = ref(null)
  
  let activity = 'x zgłoszeń (PLACEHOLDER)'
  const lastTicketDate = ref(new Date().toLocaleDateString())
  
  onMounted(() => {
    const ctx = chart.value.getContext('2d')
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Nowe', 'W trakcie', 'Zakończone'],
        datasets: [{
          data: [5, 3, 8],
          backgroundColor: ['#42b983', '#2196f3', '#9e9e9e']
        }]
      }
    })
  })
  </script>
  
  <style scoped>
  .profile-view {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  }
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin: 2rem 0;
  }
  
  .stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    text-align: center;
  }

  .gradient-purple {
  background: linear-gradient(135deg, #82ff8d, #00ff88);
  }

  .gradient-blue {
  background: linear-gradient(135deg, #7ac3ff, #2894ff);
  }
  
  .stat-value {
    font-size: 2.5rem;
    font-weight: bold;
    margin: 1rem 0;
    color: #2c3e50;
    text-shadow: 3.5px 2.5px 1.5px #0202023f;
  }
  
  .stat-label {
    color: #161616;
    font-size: 0.9rem;
  }
  
  .progress-chart {
    background: rgb(250, 250, 255);
    padding: 2rem;
    border-radius: 10px;
    margin-top: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  }

  .header {
    font-size: 1.7rem;
    margin-top: 0.45rem;
    margin-bottom: -0.4rem;
  }
  </style>