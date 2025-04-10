<script setup lang="ts">
import { ref, watch } from 'vue'
import { useTicketStore } from '../stores/ticketStore'
import type { Ticket } from '../stores/ticketStore'

const props = defineProps<{
  ticket: Ticket
}>()

const ticketStore = useTicketStore()
const status = ref<Ticket['status']>(props.ticket.status)
const isUpdating = ref(false)

watch(status, async (newStatus) => {
  if (newStatus !== props.ticket.status) {
    isUpdating.value = true
    try {
      await ticketStore.updateTicketStatus(props.ticket.id, newStatus)
    } catch {
      status.value = props.ticket.status
    } finally {
      isUpdating.value = false
    }
  }
})
</script>

<template>
  <select v-model="status" :disabled="isUpdating">
    <option value="new">Nowe</option>
    <option value="in_progress">W trakcie</option>
    <option value="resolved">Zakończone</option>
  </select>
  <span v-if="isUpdating"> (aktualizowanie...)</span>
</template>