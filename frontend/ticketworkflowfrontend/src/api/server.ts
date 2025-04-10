import axios from 'axios'

if (import.meta.env.DEV) {
  const mockTickets = [
    {
      id: 1,
      title: 'Placeholder 1',
      description: 'Opis problemu technicznego',
      status: 'new',
      category: 'HARDWARE_FAILURE',
      priority: 'medium',
      createdAt: new Date().toISOString(),
      dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
    },
    {
      id: 2,
      title: 'Placeholder 2',
      description: 'Problem z oprogramowaniem',
      status: 'in_progress',
      category: 'SOFTWARE_FAILURE',
      priority: 'high',
      createdAt: new Date().toISOString(),
      dueDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString()
    }
  ]

  axios.interceptors.request.use(config => {
    if (config.url?.endsWith('/api/tickets') && config.method === 'get') {
      return {
        ...config,
        data: mockTickets
      }
    }
    
    if (config.url?.endsWith('/api/tickets') && config.method === 'post') {
      const newTicket = {
        ...config.data,
        id: Math.max(...mockTickets.map(t => t.id)) + 1,
        status: 'new',
        createdAt: new Date().toISOString()
      }
      mockTickets.push(newTicket)
      return {
        ...config,
        data: newTicket
      }
    }
    
    if (config.url?.match(/\/api\/tickets\/\d+\/status/) && config.method === 'patch') {
      const id = parseInt(config.url.split('/')[3])
      const ticket = mockTickets.find(t => t.id === id)
      if (ticket) {
        ticket.status = config.data.status
      }
      return {
        ...config,
        data: { status: config.data.status }
      }
    }
    
    return config
  })
}