// src/stores/ticketStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export interface Ticket {
  id: number
  title: string
  description: string
  status: 'new' | 'in_progress' | 'resolved'
  category: string
  priority: 'low' | 'medium' | 'high'
  createdAt: string
  dueDate?: string
}

export const useTicketStore = defineStore('ticket', () => {
  const tickets = ref<Ticket[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const fetchTickets = async () => {
    isLoading.value = true
    try {

      tickets.value = [
        {
          id: 1,
          title: 'Zgłoszenie example (PLACEHOLDER)',
          description: 'Opis problemu',
          status: 'new',
          category: 'HARDWARE_FAILURE',
          priority: 'medium',
          createdAt: new Date().toISOString(),
          dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: 2,
          title: 'Zgłoszenie example (PLACEHOLDER)',
          description: 'Opis problemu',
          status: 'in_progress',
          category: 'SOFTWARE_FAILURE',
          priority: 'high',
          createdAt: new Date().toISOString(),
          dueDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString()
        }
      ]
      // const response = await axios.get('/api/tickets')
      // tickets.value = response.data
    } catch (err) {
      error.value = 'Błąd pobierania zgłoszeń'
      console.error(err)
    } finally {
      isLoading.value = false
    }
  }

  const createTicket = async (ticketData: Omit<Ticket, 'id' | 'createdAt' | 'status'> & { dueDate?: string }) => {
    isLoading.value = true
    try {
      const response = await axios.post('/api/tickets', {
        ...ticketData,
        status: 'new',
        createdAt: new Date().toISOString()
      })
      tickets.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = 'Błąd tworzenia zgłoszenia'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const updateTicketStatus = async (id: number, newStatus: Ticket['status']) => {
    try {
      const response = await axios.patch<{ status: Ticket['status'] }>(
        `/api/tickets/${id}/status`,
        { status: newStatus }
      )
      
      const ticket = tickets.value.find(t => t.id === id)
      if (ticket) {
        ticket.status = response.data.status
      }
    } catch (err) {
      error.value = 'Błąd aktualizacji statusu'
      console.error('Update status error:', err)
      throw err
    }
  }

  return {
    tickets,
    fetchTickets,
    createTicket,
    updateTicketStatus,
    isLoading,
    error
  }
})