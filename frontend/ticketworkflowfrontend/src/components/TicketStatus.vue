<script setup lang="ts">
import { ref, watch } from 'vue'
import { useTicketStore } from '../stores/ticketStore'
import type { Ticket } from '../stores/ticketStore'

const props = defineProps<{
  status: 'OPEN' | 'IN_PROGRESS' | 'CLOSED'
  ticketId?: number
}>()
console.log('Received status:', props.status)
const ticketStore = useTicketStore()
const localStatus = ref(props.status)
const isUpdating = ref(false)

watch(localStatus, async (newStatus) => {
  if (props.ticketId && newStatus !== props.status) {
    isUpdating.value = true
    try {
      await ticketStore.updateTicketStatus(props.ticketId, newStatus)
    } catch {
      localStatus.value = props.status
    } finally {
      isUpdating.value = false
    }
  }
})
</script>

<template>
  <span v-if="localStatus" class="status-badge" :class="localStatus.toLowerCase()">
    {{
      localStatus === 'OPEN' ? 'Otwarte' :
      localStatus === 'IN_PROGRESS' ? 'W trakcie' : 'Zamknięte'
    }}
  </span>
  <span v-else class="status-badge-error">Invalid Status</span>
</template>

<style scoped>
.status-badge {
  color: #000000;
  font-weight: bolder;
}

.status-badge.error {
  color: #ff0000;
  border: 1px dashed #ff0000;
}
</style>