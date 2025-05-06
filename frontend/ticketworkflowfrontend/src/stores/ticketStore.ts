import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { mockTickets } from '../api/server'


export interface Ticket {
  id: number
  title: string
  description: string
  category: string
  status: 'OPEN' | 'IN_PROGRESS' | 'CLOSED'
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT'
  created_at: string
  updated_at: string
  created_by: number | string | null
  of_department: number | string
  assigned: number | string | null
  due?: string,
  closed_at: string
}

export interface TicketCreate {
  title: string
  description: string
  category: string
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT'
  due?: string
  assigned?: number | null
}

export const useTicketStore = defineStore('ticket', () => {
  const tickets = ref<Ticket[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const fetchTickets = async () => {
    isLoading.value = true
    try {
      tickets.value = mockTickets;
      console.log('Using mock tickets directly');
    } catch (err) {
      error.value = 'Błąd pobierania zgłoszeń';
      console.error(err);
    } finally {
      isLoading.value = false;
    }
  }

  const createTicket = async (ticketData: TicketCreate) => {
    isLoading.value = true
    try {
      const response = await axios.post('/api/tickets/', ticketData)
      tickets.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = 'Błąd tworzenia zgłoszenia'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const updateTicket = async (id: number, ticketData: Partial<Ticket>) => {
    try {
      const response = await axios.patch(`/api/tickets/${id}/`, ticketData)
      
      const index = tickets.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tickets.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = 'Błąd aktualizacji zgłoszenia'
      console.error('Update error:', err)
      throw err
    }
  }
  
  const updateTicketStatus = async (id: number, newStatus: Ticket['status']) => {
    return updateTicket(id, { status: newStatus })
  }
  
  const deleteTicket = async (id: number) => {
    try {
      await axios.delete(`/api/tickets/${id}/`)
      tickets.value = tickets.value.filter(t => t.id !== id)
    } catch (err) {
      error.value = 'Błąd usuwania zgłoszenia'
      console.error('Delete error:', err)
      throw err
    }
  }

  return {
    tickets,
    fetchTickets,
    createTicket,
    updateTicket,
    updateTicketStatus,
    deleteTicket,
    isLoading,
    error
  }
})