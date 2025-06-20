<template>
  <router-view />
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
authStore.initializeAuth()
</script>
