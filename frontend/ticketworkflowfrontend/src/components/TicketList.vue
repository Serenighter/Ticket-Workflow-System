<template>
  <div class="ticket-list">
    <div class="header">
      <h1>Lista zgłoszeń</h1>
      <button @click="showAddForm = true" class="btn btn-primary">
        + Dodaj zgłoszenie
      </button>
    </div>

 
    <div v-if="loading || ticketStore.isLoading">Ładowanie zgłoszeń...</div>
    <div v-else-if="ticketStore.error" class="error">{{ ticketStore.error }}</div>
    <div v-else>
      <div class="refresh-section">
        <button @click="refreshTickets" :disabled="ticketStore.isLoading" class="refresh-btn">
          {{ ticketStore.isLoading ? 'Odświeżanie...' : 'Odśwież listę' }}
        </button>
        <span class="tickets-count">Znaleziono: {{ ticketStore.tickets.length }} zgłoszeń</span>
      </div>

      <table v-if="ticketStore.tickets.length > 0">
        <thead>
          <tr>
            <th>ID</th>
            <th>Tytuł</th>
            <th>Status</th>
            <th>Kategoria</th>
            <th>Priorytet</th>
            <th>Utworzone przez</th>
            <th>Akcje</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="ticket in ticketStore.tickets"
            :key="ticket.id"
          >
            <td>{{ ticket.id + "TW" }}</td>
            <td>{{ ticket.title }}</td>
            <td>{{ ticket.status_display || ticket.status }}</td>
            <td>{{ ticket.category_display || ticket.category }}</td>
            <td>{{ ticket.priority_display || ticket.priority }}</td>
            <td>{{ ticket.created_by?.username || 'Nieznany' }}</td>
            <td class="actions-cell">
              <button @click.stop="showDetails(ticket)" class="btn-details">
                Szczegóły
              </button>
              <button @click.stop="confirmDelete(ticket)" class="btn-delete">
                Usuń
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-else class="no-tickets">
        <h3>Brak zgłoszeń do wyświetlenia</h3>
        <p>Rozpocznij od dodania pierwszego zgłoszenia</p>
        <button @click="showAddForm = true" class="btn btn-primary">
          + Dodaj pierwsze zgłoszenie
        </button>
      </div>

      <div v-if="selectedTicket" class="ticket-details">
        <h2>Szczegóły zgłoszenia #{{ selectedTicket.id }}</h2>
        <p><strong>Tytuł:</strong> {{ selectedTicket.title }}</p>
        <p><strong>Opis:</strong> {{ selectedTicket.description }}</p>
        <p><strong>Status:</strong> {{ selectedTicket.status_display || selectedTicket.status }}</p>
        <p><strong>Kategoria:</strong> {{ selectedTicket.category_display || selectedTicket.category }}</p>
        <p><strong>Priorytet:</strong> {{ selectedTicket.priority_display || selectedTicket.priority }}</p>
        <p><strong>Twórca:</strong> {{ selectedTicket.created_by?.username || 'Nieznany' }}</p>
        <p><strong>Dział:</strong> {{ selectedTicket.of_department?.name || 'Brak danych' }}</p>
        <div class="actions">
          <button @click="confirmDelete(selectedTicket)" class="btn-delete">
            Usuń zgłoszenie
          </button>
          <button @click="selectedTicket = null">Zamknij</button>
        </div>
      </div>
    </div>

    <div v-if="showAddForm" class="modal-overlay" @click.self="closeForm">
      <TicketForm
        @close="closeForm"
      />
    </div>

    <div v-if="notification" class="notification" :class="notification.type">
      {{ notification.message }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTicketStore, type Ticket } from '@/stores/ticketStore'
import { useAuthStore } from '@/stores/authStore'
import TicketForm from './TicketForm.vue'
import type { TicketForm as TicketFormType } from '@/types/ticket'

const ticketStore = useTicketStore()
const authStore = useAuthStore()

const selectedTicket = ref<Ticket | null>(null)
const loading = ref(true)
const showAddForm = ref(false)
const showDebug = ref(false)
const notification = ref<{ message: string, type: 'success' | 'error' } | null>(null)

function showDetails(ticket: Ticket) {
  selectedTicket.value = ticket
}

async function refreshTickets() {
  console.log('=== REFRESH TICKETS ===')
  await ticketStore.getTickets()
}

function closeForm() {
  showAddForm.value = false
}

async function handleSubmit(formData: TicketFormType) {
  console.log('Submitting ticket:', formData)
  
  try {
    const result = await ticketStore.createTicket(formData)
    
    if (result) {
      showNotification('Zgłoszenie zostało utworzone pomyślnie!', 'success')
      closeForm()
    } else {
      showNotification('Wystąpił błąd podczas tworzenia zgłoszenia', 'error')
    }
  } catch (error) {
    console.error('Error creating ticket:', error)
    showNotification('Wystąpił błąd podczas tworzenia zgłoszenia', 'error')
  }
}

function showNotification(message: string, type: 'success' | 'error') {
  notification.value = { message, type }
  setTimeout(() => {
    notification.value = null
  }, 5000)
}

async function confirmDelete(ticket: Ticket) {
  if (confirm(`Czy na pewno chcesz usunąć zgłoszenie #${ticket.id}?`)) {
    try {
      const result = await ticketStore.deleteTicket(ticket.id)
      if (result) {
        showNotification('Zgłoszenie zostało usunięte pomyślnie!', 'success')
        
        if (selectedTicket.value && selectedTicket.value.id === ticket.id) {
          selectedTicket.value = null
        }
      } else {
        showNotification('Wystąpił błąd podczas usuwania zgłoszenia', 'error')
      }
    } catch (error) {
      console.error('Error deleting ticket:', error)
      showNotification('Wystąpił błąd podczas usuwania zgłoszenia', 'error')
    }
  }
}

onMounted(async () => {
  console.log('=== TICKET LIST MOUNTED ===')
  
  if (authStore.isAuthenticated) {
    console.log('User authenticated - getting tickets...')
    await refreshTickets()
  } else {
    console.log('User not authenticated')
  }

  loading.value = false
})
</script>

<style scoped>
.ticket-list {
  max-width: 1800px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
  padding: 0 0.5rem;
}

.header h1 {
  margin: 0;
  color: #1e293b;
  font-size: 2.5rem;
  font-weight: 300;
  letter-spacing: -0.5px;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.btn {
  padding: 0.875rem 1.75rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.btn:hover::before {
  left: 100%;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px -5px rgba(59, 130, 246, 0.4);
}

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  border-radius: 8px;
}

.refresh-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 1rem 1.25rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.refresh-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-family: inherit;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 3px 6px rgba(16, 185, 129, 0.3);
}

.refresh-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 12px rgba(16, 185, 129, 0.4);
}

.refresh-btn:disabled {
  background: linear-gradient(135deg, #9ca3af 0%, #6b7280 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tickets-count {
  font-weight: 600;
  color: #475569;
  font-size: 1.1rem;
  background: linear-gradient(135deg, #e0e7ff, #c7d2fe);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 1rem;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

th,
td {
  padding: 1rem 1.25rem;
  text-align: left;
  border-bottom: 1px solid rgba(203, 213, 225, 0.5);
}

th {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  font-weight: 700;
  color: #334155;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  position: sticky;
  top: 0;
  z-index: 10;
}

th:first-child {
  border-top-left-radius: 16px;
}

th:last-child {
  border-top-right-radius: 16px;
}

tbody tr {
  transition: all 0.2s ease;
}

tbody tr:hover {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  transform: scale(1.005);
}

tbody tr:last-child td:first-child {
  border-bottom-left-radius: 16px;
}

tbody tr:last-child td:last-child {
  border-bottom-right-radius: 16px;
}

tbody tr:last-child td {
  border-bottom: none;
}

.error {
  color: #dc2626;
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border: 1px solid #f87171;
  padding: 1rem 1.25rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  font-weight: 500;
  box-shadow: 0 4px 6px -1px rgba(220, 38, 38, 0.1);
}

.no-tickets {
  text-align: center;
  padding: 4rem 2rem;
  color: #64748b;
  background: white;
  border-radius: 20px;
  border: 2px dashed #cbd5e1;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  margin: 2rem 0;
}

.no-tickets h3 {
  margin-top: 0;
  color: #475569;
  font-size: 1.5rem;
  font-weight: 300;
  margin-bottom: 0.5rem;
}

.no-tickets p {
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.ticket-details {
  border: none;
  padding: 2rem;
  margin-top: 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border-left: 4px solid #3b82f6;
}

.ticket-details h2 {
  margin-top: 0;
  color: #1e293b;
  font-size: 1.75rem;
  font-weight: 300;
  margin-bottom: 1.5rem;
}

.ticket-details p {
  margin-bottom: 1rem;
  line-height: 1.6;
  color: #475569;
}

.ticket-details strong {
  color: #1e293b;
  font-weight: 600;
}


.actions-cell {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.btn-details {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  padding: 0.625rem 1.125rem;
  border-radius: 8px;
  cursor: pointer;
  font-family: inherit;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
}

.btn-details:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.4);
}

.btn-delete {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border: none;
  padding: 0.625rem 1.125rem;
  border-radius: 8px;
  cursor: pointer;
  font-family: inherit;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
}

.btn-delete:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(239, 68, 68, 0.4);
}

.ticket-details .actions {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.ticket-details .actions button {
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  cursor: pointer;
  font-family: inherit;
  font-weight: 600;
  transition: all 0.3s ease;
}

.ticket-details .actions button:not(.btn-delete) {
  background: linear-gradient(135deg, #64748b 0%, #475569 100%);
  color: white;
  border: none;
  box-shadow: 0 2px 4px rgba(100, 116, 139, 0.3);
}

.ticket-details .actions button:not(.btn-delete):hover {
  background: linear-gradient(135deg, #475569 0%, #334155 100%);
  transform: translateY(-1px);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.notification {
  position: fixed;
  top: 2rem;
  right: 2rem;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  font-family: inherit;
  z-index: 1001;
  animation: slideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(8px);
}

.notification.success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.notification.error {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

div:has-text("Ładowanie zgłoszeń...") {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #64748b;
  font-weight: 500;
}

@media (max-width: 768px) {
  .ticket-list {
    padding: 1rem;
  }

  .header {
    flex-direction: column;
    gap: 1.5rem;
    align-items: stretch;
    text-align: center;
  }

  .header h1 {
    font-size: 2rem;
  }
  
  .refresh-section {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  table {
    font-size: 0.9rem;
  }
  
  th, td {
    padding: 0.75rem 0.5rem;
  }

  .actions-cell {
    flex-direction: column;
    gap: 0.5rem;
    min-width: 120px;
  }

  .btn-details, .btn-delete {
    width: 100%;
    padding: 0.5rem;
    font-size: 0.8rem;
  }

  .ticket-details {
    padding: 1.5rem;
    margin: 1rem 0;
  }

  .ticket-details .actions {
    flex-direction: column;
    gap: 0.75rem;
  }

  .notification {
    top: 1rem;
    right: 1rem;
    left: 1rem;
    max-width: none;
  }
}

@media (max-width: 480px) {
  .header h1 {
    font-size: 1.75rem;
  }

  .btn {
    padding: 0.75rem 1.25rem;
    font-size: 0.9rem;
  }

  th, td {
    padding: 0.5rem 0.25rem;
    font-size: 0.85rem;
  }

  .no-tickets {
    padding: 2rem 1rem;
  }
}

</style>