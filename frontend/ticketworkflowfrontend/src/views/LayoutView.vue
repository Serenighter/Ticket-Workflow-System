<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="ticket-system">
    <header class="header">
      <h1>System zgłoszeń</h1>
    </header>
    
    <div class="layout">
      <nav class="sidebar">
        <RouterLink 
          to="/tickets" 
          class="nav-item"
          exact-active-class="active"
        >
          Lista zgłoszeń
        </RouterLink>
        
        <RouterLink 
          to="/tickets/add-ticket" 
          class="nav-item"
          active-class="active"
        >
          Dodaj zgłoszenie
        </RouterLink>
        
        <RouterLink 
          to="/tickets/profile" 
          class="nav-item"
          active-class="active"
        >
          Twój profil
        </RouterLink>
      </nav>
      
      <main class="content">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<style scoped>
.header {
  background: #2c3e50;
  color: white;
  font-family: 'Trebuchet MS';
  text-shadow: 2.5px 2.5px 1px rgba(0, 0, 0, 0.55);
  padding: 1.5rem 1rem;
  text-align: center;
  box-shadow: 0 2px 9px rgba(0, 0, 0, 0.5);
}

.header h1 {
  margin: 0;
  font-size: 1.8rem;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.layout {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 60px);
}

.sidebar {
  width: 100%;
  background: #2c3e50;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-item {
  color: white;
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  font-size: 110%;
  padding: 1rem;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.active {
  background: #42b983 !important;
  box-shadow: 2.5px 2.5px rgba(0, 0, 0, 0.425);
}

.content {
  padding: 2rem;
  flex: 1;
}

@media (min-width: 768px) {
  .layout {
    flex-direction: row;
  }
  
  .sidebar {
    width: 250px;
    min-height: 100vh;
  }
}
</style>