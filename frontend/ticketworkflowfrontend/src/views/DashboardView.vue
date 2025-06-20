<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <div class="user-info">
        <h2>Witaj, {{ user?.first_name || user?.username || 'użytkowniku' }}!</h2>
        <p>Twój dział: {{ user?.department || 'Nie przypisano' }}</p>
      </div>
      <button @click="logout" class="logout-btn">Wyloguj</button>
    </header>

    <div class="dashboard-content">

      <TicketList />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import TicketList from '@/components/TicketList.vue';

const authStore = useAuthStore();
const user = computed(() => authStore.user);

const logout = () => {
  authStore.logout();
};
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  background: (135deg, #ffffff 0%, #ffffff 100%);
  position: relative;
}

.dashboard::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 300px;
  background: (135deg, #ffffff 0%, #ffffff 50%, #ffffff 100%);
  opacity: 0.1;
  z-index: 0;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 2.5rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;
  margin: 1rem 1rem 0;
  border-radius: 20px 20px 0 0;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.user-info h2 {
  margin: 0;
  font-size: 2rem;
  font-weight: 300;
  color: #1e293b;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-info p {
  margin: 0;
  color: #64748b;
  font-size: 1.1rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  display: inline-block;
  position: relative;
  overflow: hidden;
}


.logout-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border: none;
  padding: 0.875rem 1.75rem;
  border-radius: 12px;
  cursor: pointer;
  font-family: inherit;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.3), 0 2px 4px -1px rgba(239, 68, 68, 0.1);
  position: relative;
  overflow: hidden;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.logout-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.logout-btn:hover::before {
  left: 100%;
}

.logout-btn:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px -5px rgba(239, 68, 68, 0.5), 0 4px 6px -1px rgba(239, 68, 68, 0.2);
}

.logout-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.3);
}

.dashboard-content {
  flex: 1;
  padding: 0;
  max-width: none;
  margin: 0;
  width: 100%;
  position: relative;
  z-index: 5;
  background: transparent;
}

.user-info {
  position: relative;
}



@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-5px);
  }
}

.dashboard-header {
  animation: float 6s ease-in-out infinite;
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.user-info h2 {
  background: linear-gradient(45deg, #1e293b, #3b82f6, #06b6d4, #1e293b);
  background-size: 300% 300%;
  animation: gradientShift 8s ease infinite;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}


@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    gap: 1.5rem;
    padding: 1.5rem;
    margin: 0.5rem 0.5rem 0;
    border-radius: 16px 16px 0 0;
    text-align: center;
  }

  .user-info h2 {
    font-size: 1.75rem;
  }

  .user-info p {
    font-size: 1rem;
    padding: 0.4rem 0.8rem;
  }

  .logout-btn {
    padding: 0.75rem 1.5rem;
    font-size: 0.9rem;
    width: 100%;
    max-width: 200px;
  }

  .user-info::after {
    bottom: -5px;
  }
}

@media (max-width: 480px) {
  .dashboard-header {
    padding: 1rem;
    margin: 0.25rem 0.25rem 0;
    border-radius: 12px 12px 0 0;
  }

  .user-info h2 {
    font-size: 1.5rem;
  }

  .user-info p {
    font-size: 0.9rem;
    padding: 0.3rem 0.6rem;
  }

  .logout-btn {
    padding: 0.625rem 1.25rem;
    font-size: 0.8rem;
  }
}


@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.9;
    transform: scale(1.02);
  }
}

.user-info p {
  animation: pulse 4s ease-in-out infinite;
}

.dashboard::after {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 20% 80%, rgba(178, 175, 231, 0.3) 0%, transparent 50%),
              radial-gradient(circle at 80% 20%, rgba(109, 191, 206, 0.3) 0%, transparent 50%),
              radial-gradient(circle at 40% 40%, rgba(77, 175, 142, 0.2) 0%, transparent 50%);
  pointer-events: none;
  z-index: 1;
}



.user-info:hover h2 {
  animation-duration: 2s;
}

.user-info:hover p {
  animation-duration: 2s;
  background: linear-gradient(135deg, #ddd6fe 0%, #c7d2fe 100%);
}


.logout-btn::after {
  content: '→';
  margin-left: 0.5rem;
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.logout-btn:hover::after {
  transform: translateX(3px);
}


@keyframes slideInFromTop {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dashboard-header {
  animation: slideInFromTop 0.8s ease-out;
}

.logout-btn:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.3), 0 8px 25px -5px rgba(239, 68, 68, 0.5);
}

.logout-btn:focus:not(:hover) {
  transform: none;
}
</style>