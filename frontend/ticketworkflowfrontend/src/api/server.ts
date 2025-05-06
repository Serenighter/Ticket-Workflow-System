import axios from 'axios'
import { Ticket } from '../stores/ticketStore'
import { TicketCreate } from '../stores/ticketStore'


export const mockTickets: Ticket[] = [
    {
      id: 1,
      title: 'Placeholder 1',
      description: 'Opis problemu technicznego',
      category: 'HARDWARE_FAILURE',
      status: 'OPEN',
      priority: 'MEDIUM',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      created_by: 1,
      of_department: 1,
      assigned: null,
      due: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
      closed_at: ''
    },
    {
      id: 2,
      title: 'Placeholder 2',
      description: 'Problem z oprogramowaniem',
      category: 'SOFTWARE_FAILURE',
      status: 'IN_PROGRESS',
      priority: 'HIGH',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      created_by: 2,
      of_department: 1,
      assigned: 3,
      due: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString(),
      closed_at: ''
    }
  ]

  // Mock GET /api/tickets/
  axios.interceptors.request.use(config => {
    if (config.url?.endsWith('/api/tickets/') && config.method === 'get') {
      return {
        ...config,
        adapter: () => Promise.resolve({
          data: mockTickets,
          status: 200,
          statusText: 'OK',
          headers: {},
          config: config
        })
      }
    }

    // Mock POST /api/tickets/
    if (config.url?.endsWith('/api/tickets/') && config.method === 'post') {
      const newTicket: Ticket = {
        ...config.data as TicketCreate,
        id: Math.max(...mockTickets.map(t => t.id)) + 1,
        status: 'OPEN',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        created_by: 1,
        of_department: 1,
        assigned: config.data.assigned || null,
        closed_at: ''
      }
      mockTickets.push(newTicket)
      
      return {
        ...config,
        adapter: () => Promise.resolve({
          data: newTicket,
          status: 201,
          statusText: 'Created',
          headers: {},
          config: config
        })
      }
    }

    // Mock PATCH /api/tickets/:id/status
    if (config.url?.match(/\/api\/tickets\/\d+\/status/) && config.method === 'patch') {
      const id = parseInt(config.url.split('/')[3])
      const ticket = mockTickets.find(t => t.id === id)
      if (ticket) {
        ticket.status = config.data.status
        ticket.updated_at = new Date().toISOString()
      }
      
      return {
        ...config,
        adapter: () => Promise.resolve({
          data: { status: config.data.status },
          status: 200,
          statusText: 'OK',
          headers: {},
          config: config
        })
      }
    }

    return config
  })
