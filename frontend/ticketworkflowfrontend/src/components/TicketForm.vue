<script setup lang="ts">
import { ref } from 'vue'
import { useTicketStore } from '../stores/ticketStore'

interface TicketFormData {
  title: string
  description: string
  category: string
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT'
  due?: string,
}

const form = ref<TicketFormData>({
  title: "",
  description: "",
  category: "",
  priority: 'LOW',
  due: undefined,
})

const ticketStore = useTicketStore()
const emit = defineEmits(['close'])

const submit = () => {
  if (!form.value.title.trim() || !form.value.description.trim() || !form.value.category) {
    alert('Proszę wypełnić wszystkie wymagane pola')
    return
  }

  ticketStore.createTicket({
    title: form.value.title,
    description: form.value.description,
    category: form.value.category,
    priority: form.value.priority,
    due: form.value.due
  })
  emit('close')
}
</script>

<template>
   <div class="ticket-form-wrapper">
    <button @click="$router.push('/tickets')" class="back-button">
      ← Powrót do listy
    </button>
    
    <form class="ticket-form">
    <h2>Dodaj nowe zgłoszenie</h2>
    <input v-model="form.title" placeholder="Tytuł" required>
    <textarea v-model="form.description" placeholder="Opis" required></textarea>
    <select v-model="form.category" required>
      <option value="">Wybierz kategorię</option>
      <option value="HARDWARE_FAILURE">Problem ze sprzętem</option>
      <option value="SOFTWARE_FAILURE">Problem z oprogramowaniem</option>
      <option value="DEVICE_NEEDS">Zapotrzebowanie na sprzęt</option>
    </select>
    <select v-model="form.priority">
      <option value="LOW">Niski</option>
      <option value="MEDIUM">Średni</option>
      <option value="HIGH">Wysoki</option>
    </select>
    <input 
      type="date" 
      v-model="form.due" 
      :min="new Date().toISOString().split('T')[0]"
    >
    <button type="submit">Wyślij zgłoszenie</button>
    </form>
  </div>
</template>

<style scoped>
.ticket-form {
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 500px;
  margin: 0 auto;
}
input, textarea, select {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 0.75rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.back-button {
  margin-bottom: 1rem;
  background: none;
  border: none;
  color: #42b983;
  cursor: pointer;
  padding: 0.5rem;
  font-family: 'Trebuchet MS';
}

.back-button:hover {
  text-decoration: underline;
}
</style>