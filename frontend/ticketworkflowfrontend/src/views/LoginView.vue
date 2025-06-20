<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Logowanie do systemu</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Nazwa użytkownika:</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            required
            placeholder="Wpisz swoją nazwę użytkownika"
          >
        </div>
        
        <div class="form-group">
          <label for="password">Hasło:</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required
            placeholder="Wpisz swoje hasło"
          >
        </div>
        
        <button type="submit" :disabled="isLoading" class="login-btn">
          <span v-if="isLoading">Logowanie...</span>
          <span v-else>Zaloguj się</span>
        </button>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { useTicketStore } from '@/stores/ticketStore'; // Dodaj ten import
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const ticketStore = useTicketStore(); // Dodaj tę linię
const router = useRouter();

const username = ref('');
const password = ref('');
const isLoading = ref(false);
const error = ref<string | null>(null);

const handleLogin = async () => {
  error.value = null;
  isLoading.value = true;
  
  try {
    const success = await authStore.login({
      username: username.value,
      password: password.value
    });
    
    if (success) {
      await ticketStore.getTickets();
      router.push('/dashboard');
    } else {
      error.value = authStore.error || 'Nieprawidłowa nazwa użytkownika lub hasło';
    }
  } catch (err) {
    error.value = 'Wystąpił nieoczekiwany błąd';
    console.error('Login error:', err);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  padding: 2.5rem;
  width: 100%;
  max-width: 450px;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #34495e;
}

input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
}

.login-btn {
  width: 100%;
  padding: 12px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.login-btn:hover {
  background: #2980b9;
}

.login-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 10px;
  background: #ffeef0;
  border: 1px solid #ffd1d1;
  border-radius: 6px;
  color: #e74c3c;
  text-align: center;
}
</style>