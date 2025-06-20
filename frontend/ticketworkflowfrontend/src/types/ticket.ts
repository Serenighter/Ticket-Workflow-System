export interface TicketForm {
    title: string
    description: string
    category: string
    priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT'
    due?: string
}