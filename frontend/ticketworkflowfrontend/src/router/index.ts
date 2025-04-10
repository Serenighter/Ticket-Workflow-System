import { createRouter, createWebHistory } from 'vue-router'
import TicketsView from '../views/LayoutView.vue'

const routes = [
    {
      path: '/',
      redirect: '/tickets'
    },
    {
      path: '/tickets',
      component: TicketsView,
      children: [
        {
          path: '',
          name: 'tickets',
          component: () => import('../components/TicketList.vue')
        },
        {
          path: 'add-ticket',
          name: 'add-ticket',
          component: () => import('../components/TicketForm.vue')
        },
        {
          path: 'profile',
          name: 'profile',
          component: () => import('../views/ProfileView.vue')
        }
      ]
    }
  ]
  
  const router = createRouter({
    history: createWebHistory(),
    routes
  })
  
  export default router