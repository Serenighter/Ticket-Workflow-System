<script setup lang="ts">
import { onMounted } from 'vue'
import { useTicketStore } from '../stores/ticketStore'
import TicketStatus from './TicketStatus.vue'

const ticketStore = useTicketStore()

onMounted(() => {
  ticketStore.fetchTickets()
})
</script>

<template>
  <div class="ticket-list">
    <h2>Wszystkie zgłoszenia</h2>
    
    <div 
      v-for="ticket in ticketStore.tickets" 
      :key="ticket.id" 
      class="ticket-card"
      :class="`status-${ticket.status}`"
    >
      <div class="card-header">
        <h3>{{ ticket.title }}</h3>
        <span class="priority-badge" :class="ticket.priority">
          {{ ticket.priority === 'high' ? 'Wysoki' : ticket.priority === 'medium' ? 'Średni' : 'Niski' }}
        </span>
      </div>
      
      <p class="description">{{ ticket.description }}</p>
      
      <div class="meta-info">
        <div class="meta-item">
          <span class="label">Kategoria:</span>
          <span>{{ ticket.category === 'HARDWARE_FAILURE' ? 'Problem ze sprzętem' : ticket.category === 'SOFTWARE_FAILURE' ? 'Problem z oprogramowaniem' : 'Zapotrzebowanie na sprzęt' }}</span>
        </div>
        
        <div class="meta-item">
          <span class="label">Status:</span>
          <TicketStatus :ticket="ticket" />
        </div>
        
        <div v-if="ticket.dueDate" class="meta-item">
          <span class="label">Termin:</span>
          <span class="due-date">
            {{ new Date(ticket.dueDate).toLocaleDateString('pl-PL') }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ticket-list {
  max-width: 800px;
  margin: 0 auto;
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}

.ticket-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  border-left: 4px solid;
}

.ticket-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.status-new { border-left-color: var(--secondary); }
.status-in_progress { border-left-color: #4dabf7; }
.status-resolved { border-left-color: #adb5bd; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.card-header h3 {
  font-size: 1.2rem;
  margin: 0;
  color: var(--primary);
}

.priority-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.priority-badge.high { background: #ffe3e3; color: #ff6b6b; }
.priority-badge.medium { background: #fff4de; color: #f59f00; }
.priority-badge.low { background: #d3f9d8; color: #2b8a3e; }

.meta-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.label {
  font-weight: 500;
  color: #868e96;
  min-width: 70px;
}

.empty-state {
  text-align: center;
  padding: 4rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.05);
}

.empty-state p {
  color: #868e96;
  margin-bottom: 1.5rem;
}
</style>