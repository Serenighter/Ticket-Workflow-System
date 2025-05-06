<script setup lang="ts">
import { onMounted } from 'vue'
import { useTicketStore } from '../stores/ticketStore'
import TicketStatus from './TicketStatus.vue'

const ticketStore = useTicketStore()

onMounted(() => {
  ticketStore.fetchTickets()
  console.log('Tickets after fetch: ', ticketStore.tickets)
  
})
</script>

<template>
  <div class="ticket-list">
    <h2>Wszystkie zgłoszenia</h2>
    <div v-if="ticketStore.isLoading">Loading tickets...</div>
    
    <div v-else-if="!ticketStore.tickets.length" class="empty-state">
      <p>No tickets found</p>
    </div>
    
    <div 
      v-else
      v-for="ticket in ticketStore.tickets" 
      :key="ticket.id" 
      class="ticket-card"
      :class="`status-${ticket.status?.toLowerCase() || 'unknown'}`"
    >
      <div class="card-header">
        <h3>{{ ticket.title || 'Untitled Ticket' }}</h3>
        <span v-if="ticket.priority" class="priority-badge" :class="ticket.priority.toLowerCase()">
          {{
            ticket.priority === 'HIGH' ? 'Wysoki' :
            ticket.priority === 'MEDIUM' ? 'Średni' :
            ticket.priority === 'URGENT' ? 'Pilny' : 'Niski'
          }}
        </span>
      </div>
      
      <p class="description">{{ ticket.description || 'No description provided' }}</p>
      
      <div class="meta-info">
        <div class="meta-item">
          <span class="label">Kategoria:</span>
          <span>{{ ticket.category === 'HARDWARE_FAILURE' ? 'Problem ze sprzętem' : ticket.category === 'SOFTWARE_FAILURE' ? 'Problem z oprogramowaniem' : 'Zapotrzebowanie na sprzęt' }}</span>
        </div>
        
        <div class="meta-item">
          <span class="label">Status:</span>
          <TicketStatus v-if="ticket.status" :status="ticket.status" />
          <span v-else>Unknown</span>
        </div>
        
        <div v-if="ticket.due" class="meta-item">
          <span class="label">Termin:</span>
          <span class="due-date">
            {{ new Date(ticket.due).toLocaleDateString('pl-PL') }}
          </span>
        </div>
        <div class="meta-item">
          <span class="label">Zgłoszone przez:</span>
          <span> {{ ticket.created_by + ", " + ticket.of_department }}</span>
        </div>
        
      </div>
      <div class="timestamp-footer">
          <span v-if="ticket.created_at" class="timestamp">
            Utworzono: {{ new Date(ticket.created_at).toLocaleDateString('pl-PL', { day: '2-digit', month: '2-digit', year: 'numeric' }) }}
          </span>
          <span v-if="ticket.updated_at" class="timestamp">
            Zaktualizowano: {{ new Date(ticket.updated_at).toLocaleDateString('pl-PL', { day: '2-digit', month: '2-digit', year: 'numeric' }) }}
          </span>
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
  position: relative;
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
.status-resolved { border-left-color: #18c55b; }
.status-unknown {
  border-left-color: #cccccc;
}

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

.timestamp-footer {
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid #eeeeee;
  font-size: 0.8rem;
  color: #666;
  display: flex;
  gap: 0.5rem;
  align-items: center;
  width: 100%;
}

.timestamp {
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
}

.timestamp:not(:last-child)::after {
  content: " ";
  color: #999;
  margin-left: 2.5rem;
  margin-right: 5.5rem;
}
/*mobile*/
@media (max-width: 480px) {
  .timestamp-footer {
    flex-direction: column;
    gap: 0.25rem;
    padding-top: 0.5rem;
  }
  
  .timestamp::after {
    display: none;
  }
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