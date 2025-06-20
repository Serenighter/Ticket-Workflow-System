<template>
  <div class="ticket-form">
    <div class="form-header">
      <h2>{{ isEdit ? 'Edytuj zgłoszenie' : 'Dodaj nowe zgłoszenie' }}</h2>
      <button @click="$emit('close')" class="close-btn">✕</button>
    </div>

    <form @submit.prevent="submitForm" class="form">
      <div class="form-group">
        <label for="title">Tytuł zgłoszenia *</label>
        <input
          id="title"
          v-model="form.title"
          type="text"
          required
          placeholder="Krótki opis problemu"
          :disabled="ticketStore.isLoading"
        />
      </div>

      <div class="form-group">
        <label for="description">Opis problemu *</label>
        <textarea
          id="description"
          v-model="form.description"
          required
          rows="5"
          placeholder="Szczegółowy opis problemu..."
          :disabled="ticketStore.isLoading"
        ></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="category">Kategoria *</label>
          <select
            id="category"
            v-model="form.category"
            required
            :disabled="ticketStore.isLoading"
          >
            <option value="">Wybierz kategorię</option>
            <option 
              v-for="option in categoryOptions" 
              :key="option.value" 
              :value="option.value"
            >
              {{ option.text }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="priority">Priorytet *</label>
          <select
            id="priority"
            v-model="form.priority"
            required
            :disabled="ticketStore.isLoading"
          >
            <option value="">Wybierz priorytet</option>
            <option 
              v-for="option in priorityOptions" 
              :key="option.value" 
              :value="option.value"
            >
              {{ option.text }}
            </option>
          </select>
        </div>
      </div>

      <div class="form-group" v-if="showDepartmentSelector">
        <label for="department">Dział *</label>
        <select
          id="department"
          v-model="form.of_department"
          required
          :disabled="ticketStore.isLoading || loadingDepartments"
        >
          <option value="">Wybierz dział</option>
          <option 
            v-for="dept in departments" 
            :key="dept.id" 
            :value="dept.id"
          >
            {{ dept.name }}
          </option>
        </select>
        <div v-if="loadingDepartments" class="loading-indicator">
          Ładowanie działów...
        </div>
      </div>

      <div class="form-group">
        <label for="due">Termin realizacji (opcjonalnie)</label>
        <input
          id="due"
          v-model="form.due"
          type="datetime-local"
          :disabled="ticketStore.isLoading"
        />
      </div>

      <div v-if="ticketStore.error" class="error">
        {{ ticketStore.error }}
      </div>

      <div class="form-actions">
        <button
          type="button"
          @click="$emit('close')"
          class="btn btn-cancel"
          :disabled="ticketStore.isLoading"
        >
          Anuluj
        </button>
        <button
          type="submit"
          class="btn btn-submit"
          :disabled="ticketStore.isLoading || !isFormValid"
        >
          {{ 
            ticketStore.isLoading 
              ? (isEdit ? 'Aktualizowanie...' : 'Tworzenie...') 
              : (isEdit ? 'Zaktualizuj' : 'Dodaj zgłoszenie') 
          }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useTicketStore, type TicketCreate } from '@/stores/ticketStore'
import { useAuthStore } from '@/stores/authStore'
import axios from 'axios'

interface Props {
  isEdit?: boolean
  initialData?: Partial<TicketCreate>
}

interface Department {
  id: number;
  name: string;
}

const props = withDefaults(defineProps<Props>(), {
  isEdit: false,
  initialData: () => ({})
})

const emit = defineEmits<{
  close: []
  submit: [data: TicketCreate]
}>()

const ticketStore = useTicketStore()
const authStore = useAuthStore()
const departments = ref<Department[]>([])
const loadingDepartments = ref(false)

const showDepartmentSelector = computed(() => {

  const hasUserDepartment = authStore.user?.profile?.department_id || 
                           authStore.user?.department?.id;
                           
  return !hasUserDepartment && departments.value.length > 0;
})

const form = ref<TicketCreate>({
  title: '',
  description: '',
  category: '',
  priority: 'MEDIUM',
  due: null,
  assigned: null,
  of_department: undefined
})

const isFormValid = computed(() => {

  const hasUserDepartment = authStore.user?.profile?.department_id || 
                           authStore.user?.department?.id;
  

  const hasDepartment = hasUserDepartment || form.value.of_department;
  
  return form.value.title.trim() && 
         form.value.description.trim() && 
         form.value.category && 
         form.value.priority &&
         hasDepartment
})


const categoryOptions = ref([
  { text: 'Problem z oprogramowaniem', value: 'SOFTWARE_FAILURE' },
  { text: 'Problem sprzętowy', value: 'HARDWARE_FAILURE' },
  { text: 'Zapotrzebowanie na sprzęt', value: 'DEVICE_NEEDS' },
])

const priorityOptions = ref([
  { text: 'Niski', value: 'LOW' },
  { text: 'Średni', value: 'MEDIUM' },
  { text: 'Wysoki', value: 'HIGH' },
  { text: 'Najwyższy', value: 'URGENT' }
])


async function fetchDepartments() {
  try {
    loadingDepartments.value = true;
    const token = localStorage.getItem('access_token');
    if (!token) return;

    const response = await axios.get('http://localhost:8000/api/departments/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    departments.value = response.data.results || response.data || [];
    

    if (departments.value.length > 0) {
      form.value.of_department = departments.value[0].id;
    }
  } catch (error) {
    console.error('Błąd pobierania działów:', error);
  } finally {
    loadingDepartments.value = false;
  }
}


watch(() => props.initialData, (newData) => {
  if (newData && Object.keys(newData).length > 0) {
    form.value = {
      title: newData.title || '',
      description: newData.description || '',
      category: newData.category || '',
      priority: newData.priority || 'MEDIUM',
      due: newData.due || null,
      assigned: newData.assigned || null,
      of_department: newData.of_department || undefined
    }
  }
}, { immediate: true })

async function submitForm() {
  if (!isFormValid.value) return

  try {
    if (props.isEdit) {


      emit('submit', { ...form.value })
    } else {

      const finalForm = { 
        ...form.value,
        of_department: form.value.of_department || 
                      authStore.user?.profile?.department_id ||
                      authStore.user?.department?.id
      };
      
      const result = await ticketStore.createTicket(finalForm)
      if (result) {
        emit('close')
      }
    }
  } catch (error) {

    console.error('Błąd przetwarzania zgłoszenia:', error)
  }
}


function resetForm() {
  form.value = {
    title: '',
    description: '',
    category: '',
    priority: 'MEDIUM',
    due: null,
    assigned: null,
    of_department: undefined
  }
}

onMounted(async () => {

  const hasUserDepartment = authStore.user?.profile?.department_id || 
                           authStore.user?.department?.id;
  

  if (!hasUserDepartment) {
    await fetchDepartments();
  } else {

    form.value.of_department = authStore.user?.profile?.department_id || 
                              authStore.user?.department?.id;
  }
})

defineExpose({
  resetForm
})
</script>

<style scoped>
.ticket-form {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.form-header h2 {
  margin: 0;
  color: #495057;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
  padding: 0.25rem;
  border-radius: 4px;
}

.close-btn:hover {
  background: #f8f9fa;
  color: #495057;
}

.form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #495057;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.form-group input:disabled,
.form-group select:disabled,
.form-group textarea:disabled {
  background-color: #f8f9fa;
  opacity: 0.6;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.error {
  color: #dc3545;
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  white-space: pre-line;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease-in-out;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background: #6c757d;
  color: white;
}

.btn-cancel:hover:not(:disabled) {
  background: #5a6268;
}

.btn-submit {
  background: #28a745;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background: #218838;
}

.btn-submit:disabled {
  background: #6c757d;
}

.loading-indicator {
  color: #666;
  font-style: italic;
  padding: 5px 0;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .ticket-form {
    margin: 1rem;
    max-width: calc(100% - 2rem);
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>