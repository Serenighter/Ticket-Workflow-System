export interface TicketForm {
    title: string
    description: string
    category: string
    priority: 'low' | 'medium' | 'high'
    status?: string
  }